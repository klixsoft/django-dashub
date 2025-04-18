(function ($) {

    $.fn.isInViewport = function () {
        const elementTop = $(this).offset().top;
        const elementBottom = elementTop + $(this).outerHeight();

        const viewportTop = $(window).scrollTop();
        const viewportBottom = viewportTop + $(window).height();

        return elementBottom > viewportTop && elementTop < viewportBottom;
    };

    /*
        Toggle 'open' class on click of element with class 'ps-hasmenu'
    */
    $(document).on("click", ".ps-hasmenu>.ps-link", function (e) {
        e.preventDefault();

        const parentEle = $(this).parent();
        if (parentEle.hasClass("open-menu")) {
            parentEle.find(".ps-submenu").slideUp();
            parentEle.find(".ps-arrow").css({
                transform: "rotate(0deg)"
            })
        } else {
            parentEle.find(".ps-submenu").slideDown();
            parentEle.find(".ps-arrow").css({
                transform: "rotate(90deg)"
            })
        }

        $(this).parent().toggleClass("open-menu");
    });

    const getChangeOrAddEle = (fineEle, pathname) => {
        if (pathname.includes("add")) {
            pathname = pathname.replace("/add/", "");
            return $(document).find("a[href='" + pathname + "/']");
        } else if (pathname.includes("change")) {
            pathname = pathname.replace("/change/", "");
            pathname = pathname.split('/').slice(0, -1).join('/');
            return $(document).find("a[href='" + pathname + "/']");
        }
        return fineEle;
    }

    $(document).ready(function () {
        $(document).find(".ps-item").removeClass("active");
        $(document).find(".ps-hasmenu").removeClass("open-menu active");
        const pathname = window.location.pathname;

        if (pathname) {
            let fineEle = $(document).find("a[href='" + pathname + "']");

            // Check if the path is a part of the href
            if (fineEle.length <= 0) {
                fineEle = getChangeOrAddEle(fineEle, pathname);
            }

            if (fineEle.length > 0) {
                fineEle.addClass("active");

                if (fineEle.closest("ul").hasClass("ps-submenu")) {
                    fineEle.closest(".ps-hasmenu").addClass("open-menu active");
                    fineEle.closest(".ps-submenu").slideDown();
                } else {
                    fineEle.closest(".ps-item").addClass("active");
                }

                if (!fineEle.isInViewport()) {
                    const navbarContent = $(".navbar-content");
                    if (navbarContent.length > 0) {
                        navbarContent.animate({
                            scrollTop: (fineEle.offset().top / 1.5) - navbarContent.offset().top + navbarContent.scrollTop()
                        }, 300);
                    }
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
        const sidebar = $('.ps-sidebar');
        sidebar.toggleClass("mob-sidebar-active");
        sidebar.find(".ps-menu-overlay").toggleClass("d-none");
    })

    /*
        Hide mobile sidebar and menu overlay on click of element with class 'ps-menu-overlay'
    */
    $(document).on("click", ".ps-menu-overlay", function (e) {
        e.preventDefault();
        const sidebar = $('.ps-sidebar');
        sidebar.removeClass("mob-sidebar-active");
        sidebar.find(".ps-menu-overlay").addClass("d-none");
    })

    $(document).ready(function () {
        const selectEle = $(document).find('#change-list-filters select, #changelist-form select');
        if (selectEle.length > 0) {
            selectEle.select2();
        }
    });

    $(document).on('click', '.password_field .show-hide', function () {
        const parentEle = $(this).parent();
        if (parentEle.length > 0) {
            const prevType = parentEle.find("input").attr("type");
            if (prevType === 'password') {
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

    $(document).on("click", ".addNewDocBtn", function () {
        $(document).find("#docUploadModal").modal("show");
    });

    $(document).on("click", ".alert-dismissible .close", function () {
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

    $(document).on('click', '.cancel-link', function (e) {
        e.preventDefault();
        const parentWindow = window.parent;
        if (parentWindow && typeof (parentWindow.dismissRelatedObjectModal) === 'function' && parentWindow !== window) {
            parentWindow.dismissRelatedObjectModal();
        } else {
            window.history.back();
        }
        return false;
    });

    $(document).find(".image_picker_container").each(function () {
        const observer = new MutationObserver(function (mutations) {
            mutations.forEach(function (mutation) {
                if (mutation.attributeName === "class") {
                    const element = $(mutation.target).closest(".form-group");
                    if (element.find(".errorlist").length > 0) {
                        element.find(".errorlist").remove();
                        element.find("textarea").removeClass("is-invalid");
                        updateErrorcount();
                    }
                }
            });
        });

        observer.observe(this, {attributes: true});
    });


    $(document).on("change keyup", ".form-control.is-invalid", function () {
        $(this).removeClass("is-invalid");
        $(this).closest(".form-group").find(".errorlist").remove();
        updateErrorcount();
    })

    const navbarContentEle = $('.navbar-content');
    $(".header_search_form input").on("keyup", function () {
        const value = $(this).val().toLowerCase();
        let anyVisibleItem = false;

        $(".ps-navbar .ps-item").hide();
        $(".ps-navbar .ps-caption").each(function () {
            const headingText = $(this).text().toLowerCase();
            const $heading = $(this);
            const $items = $heading.nextUntil(".ps-caption");

            let hasVisibleItems = false;

            if (headingText.includes(value)) {
                $heading.show();
                $items.show();
                hasVisibleItems = true;
            } else {
                $items.each(function () {
                    const itemText = $(this).text().toLowerCase();
                    if (itemText.includes(value)) {
                        $(this).show();
                        hasVisibleItems = true;
                    }
                });

                $heading.toggle(hasVisibleItems);
            }

            if (hasVisibleItems) {
                anyVisibleItem = true;
            }
        });

        if (!anyVisibleItem) {
            navbarContentEle.addClass("nomenu");
        } else {
            navbarContentEle.removeClass("nomenu");
        }
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

    const stackedForms = $(document).find(".stacked-inline-group");
    if (stackedForms.length > 0) {
        stackedForms.find(".panel .card-header").each(function () {
            if ($(this).parent().find(".errorlist").length <= 0) {
                if ($(this).find(".delete").length > 0) {
                    $(this).next().slideUp();
                    $(this).parent().addClass("closed");
                }
            }
        })
    }

    $(document).on("click", ".stacked-inline-group .card:not(.deleted) .card-header", function (e) {
        const card = $(this).closest('.card');
        if (card.hasClass('deleted')) {
            return;
        }

        if (!$(e.target).is('.card-tools.delete') && !$(e.target).closest('.card-tools.delete').length) {
            $(this).next().slideToggle();
            $(this).parent().toggleClass("closed");
        }
    })

    function focusAndScale(element) {
        const tab = element.closest('.tab-pane');
        const hasTabs = tab.length > 0;
        if (hasTabs) {
            const tabId = tab.attr('id');
            const tabLink = $(document).find(`a[href="#${tabId}"]`);
            tabLink.trigger("click");
        }

        if (element.find(".image_picker_container").length <= 0) {
            element.find('input, select, textarea').focus();
        }

        $('html, body').animate({
            scrollTop: element.offset().top - 100
        }, 300);
    }

    function navigateToFirstErrorField() {
        const errorList = $(document).find('.errorlist');
        if (errorList.length > 0) {
            const firstError = errorList.first();
            const errorField = firstError.closest('.form-group');
            focusAndScale(errorField);
        }
    }

    function updateErrorcount() {
        const errorList = $(document).find('.errorlist');
        if (errorList.length > 0) {
            const pageHeader = $(document).find('.page-header');
            const secondCol = pageHeader.find(".col-md-6").eq(1);
            if (secondCol.length > 0) {
                secondCol.html(`<div class="page_header_error_count">${errorList.length}</div>`)
            }
        } else {
            $(document).find(".page_header_error_count").remove();
            // $(document).find(".alert-danger").remove();
        }
    }

    function navigateToErrorField() {
        updateErrorcount();
        navigateToFirstErrorField();
    }

    $(document).on("click", ".page_header_error_count", navigateToFirstErrorField)

    $(document).ready(function () {
        navigateToErrorField();
    });

    $(document).on("change", ".card-tools.delete input[type=checkbox]", function () {
        const card = $(this).closest(".card");
        if ($(this).is(":checked")) {
            card.addClass("deleted");
        } else {
            card.removeClass("deleted");
        }
    })

    const initSortable = (selector, itemSelector) => {
        // const group = $(document).find(selector);
        // if (group.length === 0) return;

        // group.sortable({
        //     items: itemSelector
        // }).on("sortstart", function () {
        //     if (typeof tinymce !== 'undefined') tinymce.remove();
        // }).on("sortstop", function () {
        //     if (typeof tinymce !== 'undefined') {
        //         $(this).find(".tinymce").each(function () {
        //             tinymce.init(JSON.parse($(this).attr("data-mce-conf")));
        //         });
        //     }
        // });
    };

    const stackInlineGroup = $(document).find(".stacked-inline-group");
    if (stackInlineGroup.length > 0) {
        stackInlineGroup.each(function () {
            const orderField = $(this).find(".djn-item-content > fieldset > .form-row.field-order");
            console.log("FileEle", orderField)
            if (orderField.length > 0) {
                $(this).find(".djn-item-content > fieldset > .form-row.field-order").hide();
                // group.sortable({
                //     items: "div.panel:not(.empty-form)"
                // }).on("sortstart", function () {
                //     if (typeof tinymce !== 'undefined') tinymce.remove();
                // }).on("sortstop", function () {
                //     if (typeof tinymce !== 'undefined') {
                //         $(this).find(".tinymce").each(function () {
                //             tinymce.init(JSON.parse($(this).attr("data-mce-conf")));
                //         });
                //     }
                // });
            }
        })
    }

    // initSortable(".stacked-inline-group", "div.panel:not(.empty-form)");
    // initSortable(".tabular-inline-group", "tr.form-row:not(.empty-form)");

    $(document).on("click", ".djn-inline-form .djn-drag-handler", function () {
        $(this).closest(".djn-inline-form").find(".djn-item-content").slideToggle();
    })

    // Initially collapse all inline forms
    $(document).find(".djn-inline-form .djn-drag-handler").trigger("click");

    function initializeTagify() {
        const tagifyElements = $(document).find(".dashub_tag_input");
        tagifyElements.each(function () {
            if ($(this).closest(".empty-form").length <= 0) {
                const formRowEle = $(this).closest(".form-row");
                if (formRowEle.find("tags").length <= 0) {
                    const delimiter = $(this).attr("data-separator");
                    new Tagify($(this)[0], {
                        originalInputValueFormat: valuesArr => valuesArr.map(item => item.value).join(delimiter),
                        delimiters: delimiter
                    });
                }
            }
        })
    }

    initializeTagify();
    $(document).on('formset:added', initializeTagify);
})(jQuery);


