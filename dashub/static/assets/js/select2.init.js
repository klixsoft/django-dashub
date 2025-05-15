(function () {
    const $ = window.jQuery || window.django?.jQuery;
    if (!$) {
        console.error("jQuery or django.jQuery not found.");
        return;
    }

    (function ($) {
        $.fn.djangoCustomSelect2 = function () {
            $.each(this, function (i, element) {
                if (element.id.match(/__prefix__/)) {
                    return;
                }

                const ele = $(element);
                try {
                    if (ele.hasClass("select2-hidden-accessible")) {
                        ele.select2("destroy");
                    }
                } catch {
                }

                const $parent = ele.closest('.modal, .offcanvas');
                ele.select2({
                    dropdownParent: $parent.length ? $parent : null
                });
            });

            return this;
        };

        $.fn.djangoAdminSelect2 = function () {
            $.each(this, function (i, element) {
                const ele = $(element);
                try {
                    if (ele.hasClass("select2-hidden-accessible")) {
                        ele.select2("destroy");
                    }
                } catch (e) {
                    console.log(e);
                }
                const $parent = ele.closest('.modal, .offcanvas');
                ele.select2({
                    dropdownParent: $parent.length ? $parent : null,
                    ajax: {
                        data: (params) => {
                            return {
                                term: params.term,
                                page: params.page,
                                app_label: element.dataset.appLabel,
                                model_name: element.dataset.modelName,
                                field_name: element.dataset.fieldName,
                            };
                        },
                    },
                });
            });
            return this;
        };

        const noSelect2 = '.empty-form select, .select2-hidden-accessible, .selectfilter, .selector-available select, .selector-chosen select, select[data-autocomplete-light-function=select2]';
        const selectEle = $(document).find('select');
        selectEle.not(noSelect2).each(function () {
            if ($(this).hasClass('select2-hidden-accessible')) {
                $(this).select2('destroy');
            }

            $(this).djangoCustomSelect2();
        });

        $("body:not(.change-form) .admin-autocomplete")
            .not(".dashub-admin-autocomplete")
            .not("[name*=__prefix__]")
            .djangoAdminSelect2();

        document.addEventListener("formset:added", (event) => {
            $(event.target).find(".admin-autocomplete").djangoAdminSelect2();
        });
    })($);
})();
