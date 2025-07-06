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
                $(element).select2({
                    ajax: {
                        data: (params) => {
                            return {
                                term: params.term,
                                page: params.page,
                                app_label: element.dataset.appLabel,
                                model_name: element.dataset.modelName,
                                field_name: element.dataset.fieldName
                            };
                        }
                    }
                });
            });
            return this;
        };

        $("body select")
            .not(".admin-autocomplete, .selectfilter, [name*='__prefix__']")
            .djangoCustomSelect2();
        $('#filtersOffcanvas .admin-autocomplete').not('[name*=__prefix__]').djangoAdminSelect2();

        document.addEventListener("formset:added", (event) => {
            const targetEle = $(event.target);
            targetEle.find('select').not(".admin-autocomplete, .selectfilter").djangoCustomSelect2();
        });
    })($);
})();
