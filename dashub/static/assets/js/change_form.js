(function () {
    const $ = window.jQuery || window.django?.jQuery;
    if (!$) {
        console.error("jQuery or django.jQuery not found.");
        return;
    }

    (function ($) {
        'use strict';

        function updateRelatedMenusLinks(triggeringLink) {
            const $this = $(triggeringLink);
            const siblings = $this.parent().find(".change_input_links").find('.view-related, .change-related, .delete-related');
            if (!siblings.length) {
                return;
            }
            const value = $this.val();
            if (value) {
                siblings.each(function () {
                    const elm = $(this);
                    elm.attr('href', elm.attr('data-href-template').replace('__fk__', value));
                    elm.removeAttr('aria-disabled');
                });
            } else {
                siblings.removeAttr('href');
                siblings.attr('aria-disabled', true);
            }
        }

        $(document.body).on('change', '.related-widget-wrapper select', function () {
            const event = $.Event('django:update-related');
            $(this).trigger(event);
            if (!event.isDefaultPrevented()) {
                updateRelatedMenusLinks(this);
            }
        });

        const relatedMenus = $(document).find('.related-widget-wrapper select');
        if (relatedMenus.length > 0) {
            relatedMenus.each(function () {
                const event = $.Event('django:update-related');
                $(this).trigger(event);
                if (!event.isDefaultPrevented()) {
                    updateRelatedMenusLinks(this);
                }
            });
        }
    })($);
})();
