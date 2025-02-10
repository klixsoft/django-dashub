(function ($) {

    /*
        Toggle 'open' class on click of element with class 'ps-hasmenu'
    */
    $(document).on("click", ".ps-hasmenu>.ps-link", function (e) {
        e.preventDefault();

        if ($(this).parent().hasClass("open-menu")) {
            $(this).parent().find(".ps-submenu").slideUp();
        } else {
            $(this).parent().find(".ps-submenu").slideDown();
        }

        $(this).parent().toggleClass("open-menu");
    });

    $(document).ready(function () {
        $(document).find(".ps-item").removeClass("active");
        $(document).find(".ps-hasmenu").removeClass("open-menu active");
        const pathname = window.location.pathname;

        if (pathname) {
            const fineEle = $(document).find("a[href='" + pathname + "']");
            if (fineEle.length > 0) {
                fineEle.addClass("active");

                if (fineEle.closest("ul").hasClass("ps-submenu")) {
                    fineEle.closest(".ps-hasmenu").addClass("open-menu active");
                    fineEle.closest(".ps-submenu").slideDown();
                } else {
                    fineEle.closest(".ps-item").addClass("active");
                }
            }
        }
    });


    /*
        Toggle 'ps-sidebar-hide' class on click of element with id 'sidebar-hide'
    */
    $(document).on("click", "#sidebar-hide", function (e) {
        e.preventDefault();
        $(document.body).toggleClass("ps-sidebar-hide");
    })

    /*
        Toggle 'mob-sidebar-active' class and show/hide menu overlay on click of element with id 'mobile-collapse'
    */
    $(document).on("click", "#mobile-collapse", function (e) {
        e.preventDefault();
        $('.ps-sidebar').toggleClass("mob-sidebar-active");
        $('.ps-sidebar').find(".ps-menu-overlay").toggleClass("d-none");
    })

    /*
        Hide mobile sidebar and menu overlay on click of element with class 'ps-menu-overlay'
    */
    $(document).on("click", ".ps-menu-overlay", function (e) {
        e.preventDefault();
        $('.ps-sidebar').removeClass("mob-sidebar-active");
        $('.ps-sidebar').find(".ps-menu-overlay").addClass("d-none");
    })

    $(document).ready(function () {
        try {
            $(document).find('#change-list-filters select, #changelist-form select').select2();
        } catch (error) {
            console.log(error);
        }
    });

    $(document).on('click', '.password_field .show-hide', function () {
        const parentEle = $(this).parent();
        if (parentEle.length > 0) {
            const prevType = parentEle.find("input").attr("type");
            if (prevType == 'password') {
                parentEle.find("input").attr("type", "text");
                parentEle.find("input").attr("placeholder", "Password");
                parentEle.find(".show-hide").html('<i class="fa-regular fa-eye"></i>');
            } else {
                parentEle.find("input").attr("type", "password");
                parentEle.find("input").attr("placeholder", "********");
                parentEle.find(".show-hide").html('<i class="fa-regular fa-eye-slash"></i>');
            }
        }
    });

    $(document).on("click", ".addNewDocBtn", function (e) {
        $(document).find("#docUploadModal").modal("show");
    });

    $(document).on("click", ".alert-dismissible .close", function (e) {
        $(this).parent().remove();
    });

    $(document).on("click", ".horizontal_tabs .nav-link", function (e) {
        e.preventDefault();
        const target = $(this).attr("href");
        $(document).find("#jazzy-tabs .nav-link").removeClass("active");
        $(this).addClass("active");
        $(document).find(".horizontal_tabs .tab-pane").removeClass("active show");
        $(document).find(target).addClass("active show");
        if (history.pushState) {
            history.pushState(null, null, target);
        } else {
            location.hash = target;
        }
    })

    const horizontal_tabs = $(document).find(".horizontal_tabs .nav-link");
    if (horizontal_tabs.length > 0) {
        const hash = window.location.hash;
        if (hash) {
            const target = $(document).find(".horizontal_tabs .nav-link[href='" + hash + "']");
            if (target.length > 0) {
                target.click();
            }
        } else {
            horizontal_tabs.eq(0).click();
        }
    }

    const datetimes = $(document).find(".datetime");
    if (datetimes.length > 0) {
        datetimes.each(function () {
            const hasTwoinput = $(this).find("input").length > 1;
            if (hasTwoinput) {
                $(this).find("[size=10]").tempusDominus({
                    display: {
                        components: {
                            calendar: true,
                            date: true,
                            month: true,
                            year: true,
                            decades: true,
                            clock: false,
                            hours: false,
                            minutes: false,
                            seconds: false,
                            useTwentyfourHour: undefined
                        },
                        theme: "light"
                    },
                    localization: {
                        format: 'yyyy-MM-dd',
                    }
                })

                $(this).find("[size=8]").tempusDominus({
                    display: {
                        components: {
                            calendar: false,
                            date: false,
                            month: false,
                            year: false,
                            decades: false,
                            clock: true,
                            hours: true,
                            minutes: true,
                            seconds: false,
                            useTwentyfourHour: undefined
                        },
                        theme: "light"
                    },
                    localization: {
                        format: 'HH:mm:ss',
                    },
                })
            }
        })
    }

    const vDateField = $(document).find(".vDateField");
    if (vDateField.length > 0) {
        vDateField.tempusDominus({
            display: {
                components: {
                    calendar: true,
                    date: true,
                    month: true,
                    year: true,
                    decades: true,
                    clock: false,
                    hours: false,
                    minutes: false,
                    seconds: false,
                    useTwentyfourHour: undefined
                },
                theme: "light"
            },
            localization: {
                format: 'yyyy-MM-dd',
            }
        })
    }

    $('.cancel-link').click(function (e) {
        e.preventDefault();
        const parentWindow = window.parent;
        if (parentWindow && typeof (parentWindow.dismissRelatedObjectModal) === 'function' && parentWindow !== window) {
            parentWindow.dismissRelatedObjectModal();
        } else {
            window.history.back();
        }
        return false;
    });

    $(document).on("change keyup", ".form-control.is-invalid", function (e) {
        $(this).removeClass("is-invalid");
        $(this).closest(".form-group").find(".text-red").hide();
    })

    $(".header_search_form input").on("keyup", function () {
        const value = $(this).val().toLowerCase();

        $(".ps-navbar .ps-item").each(function () {
            const text = $(this).text().toLowerCase();
            const isHeading = $(this).hasClass("ps-caption");

            if (!isHeading) {
                if (text.includes(value)) {
                    $(this).show();
                } else {
                    $(this).hide();
                }
            }
        });

        $(".ps-caption").each(function () {
            const hasVisibleItems = $(this).nextUntil(".ps-caption").filter(":visible").length > 0;
            $(this).toggle(hasVisibleItems);
        });
    });

    $(document).on("change", ".search-filter", function () {
        const value = $(this).val().trim();
        const name = $(this).find("option[data-name]").eq(0).attr("data-name");
        if (value && name) {
            $(this).attr("name", name);
        } else {
            $(this).attr("name", null);
        }
    })
})(jQuery);


