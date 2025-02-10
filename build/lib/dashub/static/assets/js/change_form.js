(function ($) {
    'use strict';

    function FixSelectorHeight() {
        $('.selector .selector-chosen').each(function () {
            let selector_chosen = $(this);
            let selector_available = selector_chosen.siblings('.selector-available');

            let selector_chosen_select = selector_chosen.find('select').first();
            let selector_available_select = selector_available.find('select').first();
            let selector_available_filter = selector_available.find('p.selector-filter').first();

            selector_chosen_select.height(selector_available_select.height() + selector_available_filter.outerHeight());
            selector_chosen_select.css('border-top', selector_chosen_select.css('border-bottom'));
        });
    }

    function handleCarousel($carousel) {
        const errors = $('.errorlist li', $carousel);
        const hash = document.location.hash;

        // If we have errors, open that tab first
        if (errors.length) {
            const errorCarousel = errors.eq(0).closest('.carousel-item');
            $carousel.carousel(errorCarousel.data('carouselid'));
            $('.carousel-fieldset-label', $carousel).text(errorCarousel.data()["label"]);
        } else if (hash) {
            // If we have a tab hash, open that
            const activeCarousel = $('.carousel-item[data-target="' + hash + '"]', $carousel);
            $carousel.carousel(activeCarousel.data()["carouselid"]);
            $('.carousel-fieldset-label', $carousel).text(activeCarousel.data()["label"]);
        }

        // Update page hash/history on slide
        $carousel.on('slide.bs.carousel', function (e) {

            FixSelectorHeight();
            // call resize in change view after tab switch
            window.dispatchEvent(new Event('resize'));

            if (e.relatedTarget.dataset.hasOwnProperty("label")) {
                $('.carousel-fieldset-label', $carousel).text(e.relatedTarget.dataset.label);
            }
            const hash = e.relatedTarget.dataset.target;

            if (history.pushState) {
                history.pushState(null, null, hash);
            } else {
                location.hash = hash;
            }
        });
    }

    function handleCollapsible($collapsible) {
        const errors = $('.errorlist li', $collapsible);
        const hash = document.location.hash;

        // If we have errors, open that tab first
        if (errors.length) {
            $('.panel-collapse', $collapsible).collapse('hide');
            errors.eq(0).closest('.panel-collapse').collapse('show');

        } else if (hash) {
            // If we have a tab hash, open that
            $('.panel-collapse', $collapsible).collapse('hide');
            $(hash, $collapsible).collapse('show');
        }

        // Change hash for page-reload
        $collapsible.on('shown.bs.collapse', function (e) {

            FixSelectorHeight();
            // call resize in change view after tab switch
            window.dispatchEvent(new Event('resize'));

            if (history.pushState) {
                history.pushState(null, null, '#' + e.target.id);
            } else {
                location.hash = '#' + e.target.id;
            }
        });
    }

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
        const $carousel = $('#content-main form #jazzy-carousel');
        const $collapsible = $('#content-main form #jazzy-collapsible');

        // Ensure all raw_id_fields have the search icon in them
        $('.related-lookup').append('<i class="fa fa-search"></i>');

        // Style the inline fieldset button
        $('.inline-related fieldset.module .add-row a').addClass('btn btn-sm btn-default float-right');
        $('div.add-row>a').addClass('btn btn-sm btn-default float-right');

        // Ensure we preserve the tab the user was on using the url hash, even on page reload
        if ($carousel.length) {
            handleCarousel($carousel);
        } else if ($collapsible.length) {
            handleCollapsible($collapsible);
        }

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

    $(document.body).on('change', '.related-widget-wrapper select', function (e) {
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
