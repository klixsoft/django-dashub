(function() {

    'use strict';

    let windowRef = window;
    let windowRefProxy;
    let windowName, widgetName;
    let openerRef = windowRef.opener;
    if (!openerRef) {
        // related modal is active
        openerRef = windowRef.parent;
        windowName = windowRef.name;
        widgetName = windowName.replace(/^(change|add|delete|lookup)_/, '');
        windowRefProxy = {
            name: widgetName,
            location: windowRef.location,
            close: function() {
                openerRef.dismissRelatedObjectModal();
            }
        };
        windowRef = windowRefProxy;
    }

    // default django popup_response.js
    const initData = JSON.parse(document.getElementById('django-admin-popup-response-constants').dataset.popupResponse);
    switch (initData.action) {
        case 'change':
            if (typeof(openerRef.dismissChangeRelatedObjectPopup) === 'function') {
                openerRef.dismissChangeRelatedObjectPopup(windowRef, initData.value, initData.obj, initData.new_value);
            }
            break;
        case 'delete':
            if (typeof(openerRef.dismissDeleteRelatedObjectPopup) === 'function') {
                openerRef.dismissDeleteRelatedObjectPopup(windowRef, initData.value);
            }
            break;
        default:
            if (typeof(openerRef.dismissAddRelatedObjectPopup) === 'function') {
                openerRef.dismissAddRelatedObjectPopup(windowRef, initData.value, initData.obj);
            }
            break;
    }

})();
