'use strict';

function getCookie(name) {
    if (document.cookie && document.cookie != '') {
        const cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                const cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                return cookieValue;
            }
        }
    }
    return null;
}

async function apiCall(endpoint, httpMethod, body=null) {
    const resp = await fetch(endpoint, {
        method: httpMethod,
        body: body,
        headers: {
            'X-CSRFToken': getCookie('csrftoken')
        }
    });
    if (!resp.ok) {
        throw Error(`Server error - ${resp.statusText}`);
    }
    const respJson = await resp.json();
    if (respJson.error) {
        throw Error(`Request error - ${resp.error}`);
    }
    return respJson.result;
}

/* ajax forms */

async function ajaxFormSend(form) {
    const resp = await fetch(form.action, {
        method: form.method,
        body: new FormData(form),
    });

    if (!resp.ok) {
        throw Error(`Failed to send form ${form.action} - ${resp.statusText}`);
    }
    if (resp.headers.get('content-type') == 'application/json') {
        const respJson = await resp.json();
        if (respJson.error) {
            throw Error(`Failed to send form ${form.action} - ${respJson.error}`);
        }
        return respJson.result;
    } else {
        form.innerHTML = await resp.text();
        return null;
    }
}

async function fetchElement(element, url) {
    const resp = await fetch(url);
    if (!resp.ok) {
        throw Error(`Server error ${resp.statusText}`);
    }
    const html = await resp.text();
    element.innerHTML = html;
}

async function ajaxFormGet(form, action) {
    form.action = action;
    fetchElement(form, form.action);
}

/* Вспомогательные функции для упрощенного использования ajax-форм */

async function ajaxFormInit(form) {
    if (form.action) {
        await ajaxFormGet(form, form.action);
    }

    form.addEventListener('submit', (e) => {
        console.log('submit', form.action, form);
        e.preventDefault();
        ajaxFormSend(form).then((resp) => {
            const cb = form.dataset['cb'];
            window[cb](resp);
        });
    });
}
function initAjaxForms() {
    const ajaxForms = document.querySelectorAll('.js-ajax-form');
    ajaxForms.forEach((f) => ajaxFormInit(f));
}


/* modals */

function modalOpen(modalOverlay) {
    modalOverlay.classList.add('modal-overlay_active');
}
function modalClose(modalOverlay) {
    modalOverlay.classList.remove('modal-overlay_active');
}
function initModals() {
    const modalOpenBtns = document.querySelectorAll('.js-open-modal');
    modalOpenBtns.forEach((btn) => {
        const modalId = btn.dataset['modal'];
        btn.onclick = (e) => {
            e.preventDefault();
            const modal = document.getElementById(modalId);
            modalOpen(modal);
        };
    });

    const modalOverlays = document.querySelectorAll('.modal-overlay');
    modalOverlays.forEach((overlay) => {
        overlay.onclick = (e) => {
            if (e.target == overlay) {
                e.preventDefault();
                modalClose(overlay);
            }
        };
        /*overlay.onkeydown = (e) => {
            if (e.code == 'Escape') {
                modalClose(overlay);
            }
        };*/
    });
    document.body.addEventListener('keydown', (e) => {
        if (e.code == 'Escape') {
            modalOverlays.forEach(modalClose);
        }
    });
}

/* graph */

async function fetchGraph(ep) {
    return await apiCall(ep, 'GET');
}

function makeGraph(container) {
    const options = {
        nodes: {
            shape: 'dot',
            scaling: {
                min: 5,
                max: 30,
            },
            font: {
                color: 'white'
            }
        },
        physics: {
            forceAtlas2Based: {
                gravitationalConstant: -26,
                centralGravity: 0.005,
                springLength: 230,
                springConstant: 0.18,
            },
            maxVelocity: 146,
            solver: "forceAtlas2Based",
            timestep: 0.35,
            stabilization: { iterations: 150 },
        },
        interaction: {
            hover: true
        }
    };
    const network = new vis.Network(container, null, options);
    return network;
}

async function fetchAndUpdateGraph(network, ep) {
    const graphData = await fetchGraph(ep);
    console.log('graph', graphData);
    network.setData(graphData);
}


document.addEventListener('DOMContentLoaded', function() {
    initModals();
    initAjaxForms();
});