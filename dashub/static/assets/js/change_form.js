(function ($) {
    'use strict';

    function applySelect2() {
        const noSelect2 = '.empty-form select, .select2-hidden-accessible, .selectfilter, .selector-available select, .selector-chosen select, select[data-autocomplete-light-function=select2]';
        const selectEle = $(document).find('select');
        selectEle.not(noSelect2).each(function () {
            if ($(this).hasClass('select2-hidden-accessible')) {
                $(this).select2('destroy');
            }
        });
        selectEle.not(noSelect2).select2({width: 'element'});
    }

    $(document).ready(function () {
        applySelect2();
    });

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

    // Apply select2 to all select boxes when new inline row is created
    $(document).on('formset:added', applySelect2);
})(jQuery);
