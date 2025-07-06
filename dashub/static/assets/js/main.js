(function () {
    const $ = window.jQuery || window.django?.jQuery;
    if (!$) {
        console.error("jQuery or django.jQuery not found.");
        return;
    }

    (function ($) {
        /**
         * Check if the element is within the viewport
         * @returns {boolean}
         */
        $.fn.isInViewport = function () {
            const elementTop = $(this).offset().top;
            const elementBottom = elementTop + $(this).outerHeight();
            const viewportTop = $(window).scrollTop();
            const viewportBottom = viewportTop + $(window).height();

            return elementBottom > viewportTop && elementTop < viewportBottom;
        };

        /** ============================
         *  Menu & Sidebar Functionality
         *  ============================
         */

        // Toggle submenu visibility on click
        $(document).on("click", ".dh-hasmenu > .dh-link", function (e) {
            e.preventDefault();
            const parent = $(this).parent();
            const submenu = parent.find(".dh-submenu");
            const arrow = parent.find(".dh-arrow");

            submenu.find(".dh-item").show();
            if (parent.hasClass("open-menu")) {
                submenu.slideUp();
                arrow.css({transform: "rotate(0deg)"});
            } else {
                submenu.slideDown();
                arrow.css({transform: "rotate(90deg)"});
            }
            parent.toggleClass("open-menu");
        });

        /**
         * Handles matching for /add/ or /change/ Django admin paths
         */
        function getChangeOrAddEle(fineEle, pathname) {
            if (pathname.includes("add")) {
                pathname = pathname.replace("/add/", "");
                return $("a[href='" + pathname + "/']");
            } else if (pathname.includes("change")) {
                pathname = pathname.replace("/change/", "").split("/").slice(0, -1).join("/");
                return $("a[href='" + pathname + "/']");
            }
            return fineEle;
        }

        // Auto-highlight current nav item
        $(document).ready(function () {
            $(".dh-item, .dh-hasmenu").removeClass("active open-menu");

            const pathname = window.location.pathname;
            if (pathname) {
                let currentLink = $("a[href='" + pathname + "']");
                if (currentLink.length <= 0) {
                    currentLink = getChangeOrAddEle(currentLink, pathname);
                }

                if (currentLink.length > 0) {
                    currentLink.addClass("active");
                    const parentHasMenu = currentLink.closest(".dh-hasmenu");

                    if (parentHasMenu.length > 0) {
                        parentHasMenu.addClass("open-menu active");
                        currentLink.closest(".dh-submenu").slideDown();
                    } else {
                        currentLink.closest(".dh-item").addClass("active");
                    }

                    if (!currentLink.isInViewport()) {
                        const navbarContent = $(".navbar-content");
                        navbarContent.animate({
                            scrollTop: (currentLink.offset().top / 1.5) - navbarContent.offset().top + navbarContent.scrollTop()
                        }, 300);
                    }
                }
            }
        });

        // Sidebar toggle for desktop
        $(document).on("click", "#sidebar-hide", function (e) {
            e.preventDefault();
            $("body").toggleClass("dh-sidebar-hide");
        });

        // Sidebar toggle for mobile
        $(document).on("click", "#mobile-collapse", function (e) {
            e.preventDefault();
            const sidebar = $(".dh-sidebar");
            sidebar.toggleClass("mob-sidebar-active");
            sidebar.find(".dh-menu-overlay").toggleClass("d-none");
        });

        // Hide mobile sidebar on overlay click
        $(document).on("click", ".dh-menu-overlay", function (e) {
            e.preventDefault();
            const sidebar = $(".dh-sidebar");
            sidebar.removeClass("mob-sidebar-active");
            sidebar.find(".dh-menu-overlay").addClass("d-none");
        });

        /** ================================
         *  Password Field Toggle (Show/Hide)
         *  ================================ */
        $(document).on("click", ".password_field .show-hide", function () {
            const parent = $(this).parent();
            const input = parent.find("input");
            const type = input.attr("type");

            input.attr("type", type === "password" ? "text" : "password");
            input.attr("placeholder", type === "password" ? "Password" : "********");
            $(this).html(`<i class="fa-regular fa-eye${type === "password" ? "" : "-slash"}"></i>`);
        });

        /** ======================
         *  Modal / Alert / Tabs
         *  ====================== */

        // Show document upload modal
        $(document).on("click", ".addNewDocBtn", function () {
            $("#docUploadModal").modal("show");
        });

        // Close alert box
        $(document).on("click", ".alert-dismissible .close", function () {
            $(this).parent().remove();
        });

        // Horizontal tabs navigation
        $(document).on("click", ".horizontal_tabs .nav-link", function (e) {
            e.preventDefault();
            const target = $(this).attr("href");

            $(".horizontal_tabs .nav-link").removeClass("active");
            $(this).addClass("active");

            $(".horizontal_tabs .tab-pane").removeClass("active show");
            $(target).addClass("active show");

            if (history.pushState) {
                history.pushState(null, null, target);
            } else {
                location.hash = target;
            }
        });

        // Activate tab on load based on URL hash
        $(document).ready(function () {
            const hash = window.location.hash;
            const tabs = $(".horizontal_tabs .nav-link");

            if (hash) {
                const targetTab = tabs.filter(`[href='${hash}']`);
                if (targetTab.length) targetTab.click();
            } else {
                tabs.first().click();
            }
        });

        /** =====================
         *  DateTime Picker Setup
         *  ===================== */
        document.addEventListener("click", function (e) {
            if (e.target.classList.contains("vCheckboxLabel")) {
                const checkboxLabel = $(e.target);
                if (checkboxLabel.parent().hasClass("delete")) {
                    const cardEle = checkboxLabel.closest(".djn-item");
                    if (cardEle.length > 0) {
                        if (cardEle.hasClass("grp-predelete")) {
                            cardEle.tooltip('dispose');
                            cardEle.removeAttr('data-bs-toggle data-bs-placement title');
                        } else {
                            cardEle.find(".djn-item-content").slideUp();
                            cardEle.removeClass("open");

                            cardEle.attr({
                                'data-bs-toggle': 'tooltip',
                                'data-bs-placement': 'top',
                                'title': 'Click on save button to delete permanently'
                            });
                            cardEle.tooltip();
                        }
                    }
                }
            }
        }, true);


        const dateTimeEle = $(document).find(".datetime")
        if (dateTimeEle.length > 0) {
            dateTimeEle.each(function () {
                const hasTwoInputs = $(this).find("input").length > 1;
                if (!hasTwoInputs) return;

                $(this).find("[size=10]").tempusDominus({
                    display: {
                        components: {calendar: true, date: true, month: true, year: true, decades: true, clock: false},
                        theme: "light"
                    },
                    localization: {format: 'yyyy-MM-dd'}
                });

                $(this).find("[size=8]").tempusDominus({
                    display: {
                        components: {clock: true, hours: true, minutes: true},
                        theme: "light"
                    },
                    localization: {format: 'HH:mm:ss'}
                });
            });
        }

        const vDateFieldEle = $(document).find(".vDateField");
        if (vDateFieldEle.length > 0) {
            $(".vDateField").tempusDominus({
                display: {
                    components: {calendar: true, date: true, month: true, year: true, decades: true},
                    theme: "light"
                },
                localization: {format: 'yyyy-MM-dd'}
            });
        }

        /** ========================
         *  Form Field Error Handling
         *  ======================== */

        function updateErrorcount() {
            const errorCount = $(".errorlist").length;
            const header = $(".page-header .col-md-6").eq(1);
            if (errorCount && header.length) {
                header.html(`<div class="page_header_error_count">${errorCount}</div>`);
            } else {
                $(".page_header_error_count").remove();
            }
        }

        function focusAndScale(element) {
            if (element && element.length > 0) {
                const tab = element.closest('.tab-pane');
                if (tab.length) $(`a[href="#${tab.attr('id')}"]`).click();

                if (!element.find(".image_picker_container").length) {
                    element.find('input, select, textarea').focus();
                }

                $('html, body').animate({scrollTop: element.offset().top - 100}, 300);
            }
        }

        function navigateToFirstErrorField() {
            const errorField = $(".errorlist").first().closest('.form-group');
            focusAndScale(errorField);
        }

        function navigateToErrorField() {
            updateErrorcount();
            navigateToFirstErrorField();
        }

        $(document).on("click", ".page_header_error_count", navigateToFirstErrorField);
        $(document).ready(navigateToErrorField);

        // Clear error styles on input change
        $(document).on("change keyup", ".form-control.is-invalid", function () {
            $(this).removeClass("is-invalid").closest(".form-group").find(".errorlist").remove();
            updateErrorcount();
        });

        /** ====================
         *  Image Field Observer
         *  ==================== */
        $(".image_picker_container").each(function () {
            const observer = new MutationObserver(function (mutations) {
                mutations.forEach(mutation => {
                    if (mutation.attributeName === "class") {
                        const parent = $(mutation.target).closest(".form-group");
                        parent.find(".errorlist").remove();
                        parent.find("textarea").removeClass("is-invalid");
                        updateErrorcount();
                    }
                });
            });

            observer.observe(this, {attributes: true});
        });

        /** =========================
         *  Inline Forms & Panels
         *  ========================= */

        $(".stacked-inline-group .panel .card-header").each(function () {
            const panel = $(this).parent();
            if (!panel.find(".errorlist").length && panel.find(".delete").length) {
                $(this).next().slideUp();
                panel.addClass("closed");
            }
        });

        $(document).on("click", ".stacked-inline-group .card:not(.deleted) .card-header", function (e) {
            if ($(e.target).closest('.card-tools.delete').length) return;
            const card = $(this).closest(".card");
            card.toggleClass("closed");
            $(this).next().slideToggle();
        });

        $(document).on("click", ".cancel-link", function (e) {
            e.preventDefault();
            const parentWindow = window.parent;
            if (parentWindow && parentWindow !== window && typeof parentWindow.dismissRelatedObjectModal === 'function') {
                parentWindow.dismissRelatedObjectModal();
            } else {
                window.history.back();
            }
            return false;
        });

        /** ===================
         *  Tagify Initialization
         *  =================== */
        function initializeTagify() {
            $(document).find(".dashub_tag_input").each(function () {
                if ($(this).closest(".empty-form").length === 0) {
                    const surroundingTagsEle = $(this).parent().find("tags");
                    if (surroundingTagsEle.length <= 0) {
                        const delimiter = $(this).data("separator");
                        new Tagify(this, {
                            originalInputValueFormat: values => values.map(v => v.value).join(delimiter),
                            delimiters: delimiter
                        });
                    }
                }
            });
        }

        initializeTagify();
        $(document).on('formset:added', initializeTagify);

        /** ====================
         *  List Action Footer
         *  ==================== */
        $(document).on("change", 'input[name=_selected_action], #action-toggle', function () {
            const selectedCount = $('input[name=_selected_action]:checked').length;
            $(".change-list-actions-row").toggleClass("hide", selectedCount === 0);
        });

        /** ===================
         *  Inline Collapse Logic
         *  =================== */
        $(document).on("click", ".djn-inline-form .djn-drag-handler", function () {
            const item = $(this).closest(".djn-item");
            if (item.hasClass("grp-predelete")) return;

            const content = item.find(".djn-item-content");
            content.slideToggle();
            item.toggleClass("open");
        });

        // Collapse all on load
        $(".djn-inline-form .djn-drag-handler").trigger("click");

        /** ====================
         *  Navbar Search Filter
         *  ==================== */
        $(".header_search_form input").on("keyup", function () {
            const value = $(this).val().toLowerCase();
            let anyVisible = false;

            $(".dh-navbar .dh-item").hide();
            $(".dh-navbar .dh-caption").each(function () {
                const $heading = $(this);
                const items = $heading.nextUntil(".dh-caption");
                let showSection = false;

                if ($heading.text().toLowerCase().includes(value)) {
                    $heading.add(items).show();
                    showSection = true;
                } else {
                    items.each(function () {
                        if ($(this).text().toLowerCase().includes(value)) {
                            $(this).show();
                            showSection = true;
                        }
                    });
                    $heading.toggle(showSection);
                }

                if (showSection) anyVisible = true;
            });

            $(".navbar-content").toggleClass("nomenu", !anyVisible);
        });

        // Dynamic select name update
        $(document).on("change", ".search-filter", function () {
            const value = $(this).val().trim();
            const name = $(this).find("option[data-name]").eq(0).data("name");
            $(this).attr("name", value && name ? name : null);
        });

        const themeSwitcher = $(document).find(".theme_switcher");

        function setThemeCookie(themeChoice, resolvedTheme) {
            const expiryDate = new Date();
            expiryDate.setTime(expiryDate.getTime() + (30 * 24 * 60 * 60 * 1000));
            document.cookie = `dashub_theme=${themeChoice}; path=/; expires=${expiryDate.toUTCString()}`;
            document.cookie = `dashub_theme_resolved=${resolvedTheme}; path=/; expires=${expiryDate.toUTCString()}`;
        }

        function getThemeCookie() {
            const cookies = document.cookie.split(';');
            const themeChoice = cookies.find(cookie => cookie.trim().startsWith('dashub_theme='))?.split('=')[1];
            const resolvedTheme = cookies.find(cookie => cookie.trim().startsWith('dashub_theme_resolved='))?.split('=')[1];
            return {themeChoice, resolvedTheme};
        }

        function getSystemTheme() {
            return window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
        }

        function handleChangeInTinymce(theme) {
            if (window.tinymce && tinymce.activeEditor) {
                const dom = tinymce.activeEditor.dom;
                const htmlElement = dom.select('html')[0];

                if (htmlElement) {
                    dom.setAttrib(htmlElement, 'data-bs-theme', theme);
                }
            }
        }

        function getCurrentTheme() {
            const systemTheme = getSystemTheme();
            const currentThemeChoice = themeSwitcher.val() || "system";
            const currentTheme = currentThemeChoice === "system" ? systemTheme : currentThemeChoice;

            return {
                currentTheme,
                currentThemeChoice
            }
        }

        function handleThemeChange() {
            const {currentTheme, currentThemeChoice} = getCurrentTheme();
            document.documentElement.setAttribute("data-bs-theme", currentTheme);
            handleChangeInTinymce(currentTheme);
            setThemeCookie(currentThemeChoice, currentTheme);
        }

        function initializeTheme() {
            const {themeChoice, resolvedTheme} = getThemeCookie();
            const systemTheme = getSystemTheme();

            let finalTheme;
            let needUpdate = false;

            if (themeChoice === 'system') {
                finalTheme = resolvedTheme || systemTheme;
                needUpdate = true;
            } else {
                finalTheme = themeChoice || 'system';
                if (finalTheme === 'system') {
                    finalTheme = systemTheme;
                    needUpdate = true;
                }
            }

            document.documentElement.setAttribute("data-bs-theme", finalTheme);
            if (themeSwitcher.length) {
                themeSwitcher.val(themeChoice || 'system');
            }

            if (needUpdate) {
                setThemeCookie(themeChoice || 'system', finalTheme);
            }
        }

        initializeTheme();

        window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', handleThemeChange);
        themeSwitcher.change(handleThemeChange);

        if (window.tinymce) {
            tinymce.on('AddEditor', function (e) {
                const editor = e.editor;
                editor.on('init', function () {
                    const {currentTheme} = getCurrentTheme();
                    editor.dom.setAttrib(editor.getDoc().documentElement, 'data-bs-theme', currentTheme);
                });
            });
        }
    })($);
})();
