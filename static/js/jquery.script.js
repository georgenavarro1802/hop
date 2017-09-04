;
(function ($, window, document, undefined) {

    'use strict';


    var PRO = window.PRO || {};


    var $proSearch, $proFixedHeader, $proMainMenu, $proFooter, $proFixedMenu, $proIsDevice, $proUnderDesk, $webuild_masthead, $webuild_has_admin_bar, $proSlider;


    PRO.vars = function () {

        $proSearch = document.getElementById('sb-search');

        $proMainMenu = $('.main-navigation');

        $proFixedHeader = (webuild_ajax.sticky) ? true : false;

        $proFooter = $('footer');

        $proSlider = $('.pro-slider');

        $proFixedMenu = $('#header-sticky');

        $webuild_masthead = $('#masthead');

        $proIsDevice = ( navigator.userAgent.match(/(Android|webOS|BlackBerry|iPod|iPhone|iPad|Opera Mini)/) ) ? true : false;

        $webuild_has_admin_bar = ( $('body').hasClass('admin-bar') ) ? true : false;

    };

    PRO.dynamicVars = function () {

        $proUnderDesk = ($(window).width() < 1024) ? true : false;

    }

    PRO.loadScreen = function () {

        //Hide Website PreLoader

        $("#preloader").addClass('preloader_animation');

        //remove Preloader div

        setTimeout(function () {

            $('#preloader').remove();

        }, 2000);

    }

    PRO.menuSetup = function () {

        // top moving bar

        $proMainMenu.lavaLamp({

            easing: 'easeOutBack'

        });


        $proMainMenu.superfish({

            delay: 0,

            animation: {opacity: '1'},

            animationOut: {opacity: '0'},

            speed: 380,

            speedOut: 200,

            cssArrows: false,

        });

        // accordian menu

        var $mobileMenu = $('#mobile-menu');

        if ($proMainMenu.hasClass('accordion-menu') || $mobileMenu.length > 0) {

            if (!$mobileMenu.hasClass('already-slidedown')) {

                $('.accordion-menu ul').proAccordionFunc();

            }
            ;

            $(".menu-open").click(function () {

                $(this).fadeOut(0);

                $(".menu-close").fadeIn(100);

                $(".accordion-menu").slideDown(300).animate({top: '77px'}, ("slow"));

            });


            $(".menu-close").click(function () {

                $(this).fadeOut(0);

                $(".menu-open").fadeIn(100);

                $(".accordion-menu").animate({top: '70px'}, ("slow")).slideUp(300);

            });

        }


    }

    PRO.compactMenuSetup = function () {

        $("#compact-menu-toggle-open").click(function () {

            $(this).fadeOut(0);

            $("#compact-menu-toggle-close").fadeIn(100);

            $(".menu-compact #top-menu  .header-top").animate({width: '100%'}, (500));

            $(".compact-fade").delay(500).fadeIn(500);

        });

        $("#compact-menu-toggle-close").click(function () {

            $(this).fadeOut(0);

            $("#compact-menu-toggle-open").fadeIn(0);

            $(".menu-compact #top-menu  .header-top").delay(100).animate({width: '250px'}, (300));

            $(".compact-fade").delay(0).fadeOut(100);

        });

    }

    PRO.miscSetup = function () {

        $proFooter.find('.arrow-to-top').click(function (e) {

            $('html, body').animate({scrollTop: 0}, 800);

            return false;

        });

    }

    PRO.proTestimonial = function () {


        if ($.jqexists('royalSlider')) {


            $('.testimonialSlider').royalSlider({

                autoHeight: true,

                arrowsNav: false,

                fadeinLoadedSlide: true,

                controlNavigation: 'bullets',

                imageScaleMode: 'none',

                imageAlignCenter: false,

                loop: true,

                loopRewind: true,

                usePreloader: false,

                transitionSpeed: 500,

                easeInOut: 'easeInOutExpo',

                easeOut: 'easeInOutExpo',

                autoPlay: {

                    enabled: true,

                    pauseOnHover: true,

                    delay: 5000, // 5sec

                }

            });


        }


    };


    PRO.fixedHeader = function () {

        if ($proFixedHeader && !$proIsDevice && !webuild_ajax.sideMenu && !$proUnderDesk) {

            var headerHeight = $('header').outerHeight();

            var $fixedHeader = $('#header-sticky');

            //var $logo = $('#header-sticky .logo');

            //var $others = $('#header-sticky .cart-info, #header-sticky .search-container, #header-sticky .primary-menu .navbar-nav > li > a');

            //var fixedHeaderHeight = $fixedHeader.outerHeight();

            //var animateHeight = fixedHeaderHeight + 25;

            //var animateLogo = fixedHeaderHeight - 22;

            //var animateOthers = fixedHeaderHeight + 13;

            if ($('#wpadminbar').length > 0) {

                var adminbar = $('#wpadminbar').height();

                $fixedHeader.css('top', adminbar + 'px');

                //headerHeight = headerHeight + adminbar;

            }


            $(window).scroll(function () {

                if ($(window).scrollTop() > headerHeight) {

                    if (!$fixedHeader.is(':visible')) {

                        //$logo.css('line-height',animateLogo+'px');

                        //$others.css({'line-height':animateOthers+'px','height':animateOthers+'px'});

                        //$fixedHeader.height(animateHeight).show();

                        $fixedHeader.fadeIn('fast');

                        /*

                         // transition in css

                         //$fixedHeader.height(fixedHeaderHeight)

                         //$logo.css('line-height',fixedHeaderHeight+'px');



                         $fixedHeader.animate({

                         height: fixedHeaderHeight+'px', // to be changed

                         }, 500, "linear"

                         );

                         $logo.animate({

                         'line-height' : fixedHeaderHeight+'px', // to be changed

                         }, 500, "linear"

                         );

                         changed

                         */

                        /*$others.animate({

                         'line-height' : fixedHeaderHeight+'px', // to be changed

                         'height' : fixedHeaderHeight+'px'

                         }, 500, "linear"

                         );*/

                        $fixedHeader.addClass('fixed');

                    }

                } else {

                    $fixedHeader.hide().removeClass('fixed');

                }

            })

        }

    }

    // SHORTCODES

    PRO.proTab = function () {

        $(document).on('click.bs.tab.data-api', '.bs-tab-nav a', function (e) {

            e.preventDefault();

            $(this).tab('show');

        });

    };

    PRO.proAccordion = function () {


        $('.pro-accordions').each(function () {


            var $this = $(this),

                $wrap = $this.find('.pro-accordion');


            $wrap.each(function () {


                var $accordion = $(this),

                    $content = $accordion.find('.pro-accordion-content');


                $accordion.on('click', '.pro-accordion-title:not(.selected)', function (e) {

                    e.preventDefault();


                    $wrap.find('.pro-accordion-title').removeClass('selected');

                    $(this).addClass('selected');


                    $this.find('.pro-accordion-content:visible').slideUp(250, 'easeInOutExpo');

                    $content.slideDown(250, 'easeInOutExpo');


                });


            });


        });


    };


    PRO.proToggle = function () {


        $('.pro-toggle').each(function () {


            var $this = $(this),

                $content = $this.find('.pro-toggle-content');


            $this.on('click', '.pro-toggle-title', function (e) {

                e.preventDefault();

                $content.slideToggle(250, 'easeInOutExpo');

                $(this).toggleClass('selected');

            });


        });


    };

    PRO.proAlert = function () {


        $('.pro-alert-dismissable').each(function () {

            var $this = $(this);

            $this.on('click', '.pro-alert-close', function (e) {

                e.preventDefault();

                $this.slideUp(250, 'easeInOutExpo');

            });

        });


    };

    PRO.proFaq = function () {


        $(".pro-faq").each(function () {


            var $faq = $(this),

                $faq_filter = $faq.find('.pro-faq-filter a'),

                $faq_iso = $faq.find('.pro-faq-isotope');


            $faq_iso.isotope({

                containerClass: '',

                hiddenClass: 'pro-faq-hidden',

                animationEngine: 'best-available',

                itemClass: 'pro-faq-item',

                transformsEnabled: false,

                resizesContainer: false,

                hiddenStyle: {},

                visibleStyle: {},

                containerStyle: {},

            });


            $faq_filter.click(function (e) {


                e.preventDefault();


                var $filter = $(this);


                $filter.addClass('active').siblings().removeClass('active');

                $faq_iso.isotope({filter: $filter.attr('data-filter')});


            });


        });


    };

    PRO.bsToolTip = function () {


        $('[data-toggle=tooltip]').tooltip();


        $('.pro-tooltip-trigger').each(function () {


            var $this = $(this);


            $($this.data('selector')).tooltip({

                title: $this.html(),

                placement: $this.data('placement'),

                trigger: $this.data('trigger'),

                html: true,

                container: 'body',

            });


        });


    };


    PRO.wordRotate = function () {

        $('.pro-word-rotator').each(function (index, element) {

            var $el = $(this)


            var itemsWrapper = $el.find(".word-rotate-items");

            var items = itemsWrapper.find("> span");

            var firstItem = items.eq(0);

            $el.width(firstItem.width());

            var firstItemClone = firstItem.clone().css({'display': 'block', 'margin-bottom': itemHeight + 'px'});

            var itemHeight = firstItem.height();

            var currentItem = 1;

            var currentTop = 0;

            var widths = [];

            itemsWrapper.find("> span").each(function (index, element) {

                widths[index] = $(this).width();

                $(this).css({'display': 'block', 'margin-bottom': itemHeight + 'px'});

            });

            itemsWrapper.append(firstItemClone);

            var delay = $el.attr('data-delay');

            $el

                .height(itemHeight)

                .addClass("active");

            setInterval(function () {

                currentTop = (currentItem * (itemHeight * 2));

                $el.width(widths[currentItem]) // as it is 0 based

                itemsWrapper.animate({

                    top: -(currentTop) + "px"

                }, 300, "easeOutQuad", function () {


                    currentItem++;


                    if (currentItem > items.length) {


                        itemsWrapper.css("top", 0);

                        $el.width(widths[0])

                        currentItem = 1;


                    }


                });


            }, delay);

        });

    };

    PRO.portfolioWidthHeightFix = function (container) {

        $('.portfolio-item-info', container).each(function () {

            var $this = $(this),

                $elem = $this.find('.portfolio-item-hover'),

                el_width = $this.outerWidth(true),

                el_height = $this.outerHeight(true);

            $elem.css({"height": el_height, "width": el_width});

        });


    };

    PRO.isotopeInitalize = function () {


        $('.isotope-container').each(function () {

            var $this = $(this),

                $iso = $this.find('.isotope-loop'),

                $iso_loader = $this.find('.isotope-loading'),

                $iso_wrapper = $this.find('.isotope-wrapper'),

                $iso_filter = $this.find('.isotope-filter a'),

                $iso_item = $this.find('.isotope-item');


            $iso_loader.show();

            $iso.imagesLoaded(function () {

                setTimeout(function () {


                    $iso_loader.hide();

                    $iso_wrapper.addClass('isotope-loaded');

                    $iso_item.waypoint(function () {

                        $(this).addClass('in');

                    }, {

                        offset: "95%",

                        triggerOnce: false

                    });


                }, 300);


                PRO.portfolioWidthHeightFix($iso_item);


                $iso.isotope({

                    animationEngine: 'best-available',

                    layoutMode: $iso.data('layout') || 'masonry',

                });


                $(window).on('debouncedresize', function () {


                    setTimeout(function () {

                        PRO.portfolioWidthHeightFix($iso_item);

                        $iso.isotope('reLayout');

                        $(window).resize();

                    }, 300);


                });


            });


            $iso_filter.click(function (e) {

                e.preventDefault();


                $(this).addClass('active').siblings().removeClass('active');

                $iso_item.addClass('in');


                var selector = $(this).attr('data-filter');

                $iso.isotope({filter: selector});

            });


            $('blockquote.twitter-tweet', $iso).bind("proEventResize", function () {

                $iso.isotope('reLayout');

            });


        });


    };


    PRO.ajaxPagination = function () {


        $('.ajax-load-more').each(function () {


            var $this = $(this),

                $container = $this.parent().parent().find('.isotope-loop'),

                token = $this.data('token'),

                settings = window['webuild_load_more_' + token],

                is_isotope = parseInt(settings.isotope),

                paging = 1,

                flood = false,

                ajax_data;


            $this.bind('click', function () {


                if (flood === false) {

                    paging++;

                    flood = true;


                    // set ajax data

                    ajax_data = $.extend({}, {action: "ajax-pagination", paged: paging}, settings);


                    $.ajax({

                        type: "POST",

                        url: webuild_ajax.ajaxurl,

                        data: ajax_data,

                        dataType: "html",

                        beforeSend: function () {

                            $this.addClass('more-loading');

                        },

                        success: function (html) {


                            var content = $(html).css('opacity', 0);


                            if (is_isotope) {

                                $container.append(content);

                            } else {

                                $(content).insertBefore($this.parent());

                            }


                            $container.imagesLoaded(function () {


                                if ($.jqexists('mediaelementplayer')) {

                                    $('video, audio').mediaelementplayer();

                                }


                                if (is_isotope) {


                                    $container.isotope('appended', content);

                                    $container.isotope('reLayout');


                                    $('blockquote.twitter-tweet').bind("proEventResize", function () {

                                        $container.isotope('reLayout');

                                    });


                                    PRO.portfolioWidthHeightFix($container);


                                } else {


                                    content.animate({'opacity': 1}, 250, 'easeInOutExpo');

                                    PRO.portfolioWidthHeightFix($container);


                                }


                                // load button affecting after images loaded

                                $this.removeClass('more-loading');

                                if (parseInt(settings.max_pages) == paging) {
                                    $this.hide();
                                }


                            });


                            flood = false;


                        }

                    });


                }


                return false;

            });


        });


    };


    PRO.ajaxPortfolio = function () {


        $('.portfolio-model-ajax').each(function () {

            var $this = $(this),

                $loader = $this.find('.pro-loader'),

                $container = $this.find('.ajax-portfolio-container'),

                $content = $this.find('.ajax-content'),

                _current = 0;


            $this.on('click', '.item-ajax-load', function (e) {

                e.preventDefault();


                var $project = $(this),

                    _project_id = $project.data('post-id'),

                    _scrollTop = parseInt($this.offset().top) - 130;


                // protected for same project load

                if (_current == _project_id) {
                    return;
                }


                // check if project-opened

                if ($container.hasClass('project-opened')) {

                    $container.removeClass('project-opened');

                }


                $.ajax({

                    type: "POST",

                    url: webuild_ajax.ajaxurl,

                    data: {

                        action: 'ajax-portfolio',

                        id: _project_id

                    },

                    dataType: "html",

                    beforeSend: function () {

                        $loader.fadeIn();

                        $('body,html').animate({scrollTop: _scrollTop}, 500, 'easeInOutExpo');

                    },

                    success: function (html) {


                        var _obj = $content.html(html);

                        _obj.imagesLoaded(function () {

                            $container.addClass('project-opened');

                            _current = _project_id;

                        });


                        if ($.jqexists('mediaelementplayer')) {

                            $('video, audio').mediaelementplayer();

                        }


                    },

                    complete: function () {

                        $loader.hide();

                    }

                });


            });


            $this.on('click', '.ajax-close', function (e) {

                e.preventDefault();

                $container.removeAttr('data-post-id').removeClass('project-opened');

                _current = 0;

            });


        });


    };

    PRO.onePage = function () {

        var _offset = 72;

        if ($webuild_has_admin_bar) {

            _offset = _offset + 32;

        }


        $('.pro-scrollto').each(function () {

            $(this).on('click', function (e) {

                e.preventDefault();

                $.scrollTo($(this).attr('href'), 1000, {offset: -_offset, easing: 'easeInOutExpo'});

            });

        });


        if ($('body').hasClass('page-template-page-templatespage-one-page-php')) {


            var _header_height = parseInt($webuild_masthead.outerHeight(true) + $webuild_masthead.offset().top),

                _adminbar_height = parseInt($('#wpadminbar').outerHeight(true)) || 0,

                _sticky_height = $proFixedMenu.height(),

                $navigation = $('.menu-class, #mobile-menu, #pro-fixed-nav'),

                $fixed_nav = $('#pro-fixed-nav'),

                _waypoint_offset = _header_height,

                page_ids = $.makeArray(),

                header_before = $.exists('#header-before'),

                count = 0;


            $fixed_nav.css('margin-top', -Math.floor($fixed_nav.outerHeight(true) / 2));


            $('.logo a').click(function (e) {

                e.preventDefault();

                $.scrollTo(0, 1000, {easing: 'easeInOutExpo'});

            });

            $navigation.localScroll({

                target: 'body',

                queue: true,

                duration: 1000,

                hash: true,

                easing: 'easeInOutExpo',

                onBefore: function (e, anchor, $target) {


                    if ($proUnderDesk) {

                        this.offset = 0;

                    } else if ($(anchor).offset().top > _header_height || header_before) {

                        this.offset = -( _sticky_height + _adminbar_height );

                    } else {

                        this.offset = -_header_height;

                    }


                    _waypoint_offset = -this.offset;


                },

            });

        }

    };

    PRO.widgetTabs = function () {

        $('.tabs-widget .tabset li a').click(function (e) {

            e.preventDefault();

        });

        $('.tabs-widget').each(function () {

            $(this).find('.tabset li:first').addClass('active').show(); //Activate first tab

            $(this).find('.tab_content:first').show(); //Show first tab content

        });

        $('.tabs-widget .tabset li').click(function (e) {

            var tab_to_activate = $(this).find('a').attr('href');

            console.log(tab_to_activate);

            $(this).parent().find(' > li').removeClass('active'); //Remove all 'active' classes

            $(this).addClass('active'); // Add 'active' class to selected tab


            $(this).parents('.tabs-widget').find('.tab_content').hide(); //Hide all tab content

            $(this).parents('.tabs-widget').find(tab_to_activate).fadeIn(); //Fade in the new active tab content

        });

    };

    PRO.openSearch = function () {

        var $openSearch = $('.open-search'),

            $searchCont = $('.search-box'),

            $closeSearch = $('.close-box')

        $openSearch.click(function () {

            $searchCont.addClass('active-box');

            //$('#search-field').focus();

            setTimeout(function () {

                $('#search-field').focus();

            }, 300);

        })

        $closeSearch.click(function () {

            $searchCont.removeClass('active-box')

        })

    }

    PRO.footerEffect = function () {

        if (!webuild_ajax.footerForm && !$proUnderDesk && webuild_ajax.showFooter && webuild_ajax.footerEffect) {

            $('#content-wrapper, footer').addClass('fixed-footer');

            var marginTop = $('footer').outerHeight();

            $('#content-wrapper').css('margin-bottom', marginTop + 'px')

        }

    }

    PRO.footerSelectMenu = function () {

        // Create the dropdown base 12.02.14

        $("<select />").prependTo(".mini-nav .menu-select");


        // Create default option "Select"

        $("<option />", {

            "selected": "selected",

            "value": "",

            "text": "â€”â€”â€”"

        }).appendTo(".mini-nav .menu-select select");


        // Populate dropdown with menu items

        $(".mini-nav").each(function () {

            var elPar = $(this),

                thisSelect = elPar.find("select");

            $("a", elPar).each(function () {

                var el = $(this);

                $("<option />", {

                    "value": el.attr("href"),

                    "text": el.text(),

                    "data-level": el.attr("data-level")

                }).appendTo(thisSelect);

            });

        });


        $(".mini-nav select").change(function () {

            window.location = $(this).find("option:selected").val();

        });

        $(".mini-nav select option").each(function () {

            var $this = $(this),

                winHref = window.location.href;

            if ($this.attr('value') == winHref) {

                $this.attr('selected', 'selected');

            }
            ;

        })


        /*!-Appearance for custom select*/

        $(' .mini-nav select').each(function () {

            $(this).customSelect();

        });

        $(".menu-select select, .mini-nav .customSelect1").css("visibility", "visible");


    }

    PRO.shopTooltip = function () {

        $('.yith-wcwl-add-to-wishlist a').each(function () {

            roadtip(jQuery(this));

        });

        $('.compare-button a').each(function () {

            roadtip(jQuery(this));

        });

        $('.add-to-cart a').each(function () {

            roadtip(jQuery(this));

        });

    }


    PRO.fancybox = function () {


        $('.gallery-fancybox a, .fancybox-thumb').fancybox({

            beforeLoad: function () {

                if (!this.title.length) {

                    this.title = this.element.find('img').attr('alt');

                }

            },

            arrows: true,

            padding: 7,

            helpers: {

                media: {},

                buttons: {},

                thumbs: {

                    width: 60,

                    height: 50,

                    source: function (item) {


                        var href, thumb;


                        thumb = $(item.element).data('thumbnail');


                        if (item.element) {

                            href = $(item.element).find('img').attr('src');

                        }


                        if (!href && item.type === 'image' && item.href) {

                            href = item.href;

                        }


                        if (thumb) {

                            href = thumb;

                        }


                        return href;


                    }

                }

            }

        });


        $('.fancybox').fancybox({

            beforeLoad: function () {

                if (!this.title.length) {

                    this.title = this.element.find('img').attr('alt');

                }

            },

            padding: 7,

            helpers: {

                media: {}

            }

        });


    };

    PRO.matchHeightVC = function () {
        $('.equal_height_column').matchHeight();
    };

    PRO.shopCart = function () {

        var $cartIcon = $('.shopping-cart'),

            cont = $('.hover-helper'),

            $cartItems = $('.cart-items-container');

        $(document).on('click', '.shopping-cart', function (e) {

            e.preventDefault();

            $(this).parent('.hover-helper').toggleClass('active');

        })

        // hide on click anywhere outside

        $(document).mouseup(function (e) {

            var container = $(".hover-helper");

            if (!container.is(e.target) && container.has(e.target).length === 0) {

                container.removeClass('active');

            }

        });


        // remove item from cart

        $(document).on('click', '.ajax-remove-item', function (e) {

            e.preventDefault();


            var $thisbutton = $(this);


            var data = {

                action: 'woocommerce_remove_from_cart',

                remove_item: $thisbutton.attr('rel')

            };


            $.post(woocommerce_params.ajax_url, data, function (response) {


                var fragments = response.fragments,

                    cart_hash = response.cart_hash;


                if (fragments) {

                    $.each(fragments, function (key, value) {

                        console.log(key + '|' + value);

                        $(key).replaceWith(value);

                    });

                }


            });


        });

    }

    //////////////////////////////////////////////////////////////////////////////////////////////////////
    // PARALLAX
    //////////////////////////////////////////////////////////////////////////////////////////////////////
    var parallax = {

        selector: 'div[data-stellar-ratio]',

        init: function () {

            if ($proIsDevice || !$(this.selector).length) {
                return;
            }

            $(window).stellar({
                horizontalScrolling: false,
                verticalOffset: 0,
                horizontalOffset: 0,
                responsive: true,
                scrollProperty: 'scroll',
                positionProperty: 'transform',
                parallaxBackgrounds: false,
                parallaxElements: true,
                hideDistantElements: false,
            });
            parallax.settings();
            $(window).resize(function () {
                parallax.settings();
            });
        },
        settings: function () {

            $(parallax.selector).each(function () {
                var $parallax = $(this),
                    $container = $parallax.parent(),
                    containerHeight = $container.outerHeight(),
                    windowHeight = $(window).height();

                $parallax.css({
                    'height': containerHeight + windowHeight * 0.35,
                    'top': 0
                });
            });
        }
    };


    /*
     ////////////////////////////////////////////////////////////////////////////////////////////////////
     TITLE PARALLAX
     ////////////////////////////////////////////////////////////////////////////////////////////////////
     */

    var titleParallax = {


        selector: '.title-wrapper',

        container: '.page-title-cont',


        init: function () {

            if ($proIsDevice || $(this.container).data('effect') != 'parallax') {

                return;

            }

            $(window).scroll(function () {

                titleParallax.update();

            });

        },

        update: function () {

            var offset = $webuild_masthead.outerHeight(true),

                factor = 0;

            if ($proSlider) {

                offset = offset + $proSlider.outerHeight(true);

            }

            if ($(window).scrollTop() > offset) {

                factor = $(window).scrollTop() - offset;

                $(this.selector).transition({y: factor * .5}, 0)

                    .css('opacity', 1 - ( factor * .002 ));

            } else {

                $(this.selector).transition({y: 0}, 0)

                    .css('opacity', 1);

            }

        }

    };


    // helper functions

    $.fn.proAccordionFunc = function () {

        var $next,

            parents = this.find('.menu-item-has-children.no-link a, .menu-item-has-children > i.drop');


        parents.on("click", function (e) {

            if (e.target.nodeName == "I") {

                $next = $(this).next();

            } else {

                e.preventDefault();

                $next = $(this).siblings('ul.sub-menu');

            }


            $next.slideToggle();

            $(this).parent().toggleClass('open');

        });

    };

    function roadtip(element) {

        var tipText = element.html();

        element.bind('mouseover', function () {

            if (jQuery('.roadtip').length == 0) {

                element.before('<span class="roadtip">' + tipText + '</span>');


                var tipWidth = jQuery('.roadtip').outerWidth();

                var tipPush = -(tipWidth / 2 - element.outerWidth() / 2);

                jQuery('.roadtip').css('margin-left', tipPush);

            }

        });

        element.bind('mouseleave', function () {

            jQuery('.roadtip').remove();

        });

    }


    $(document).ready(function () {
        PRO.vars();

        PRO.dynamicVars();

        PRO.menuSetup();

        if (webuild_ajax.compactMenu) {

            PRO.compactMenuSetup();

        }

        PRO.miscSetup();

        PRO.fixedHeader();

        PRO.proTab();

        PRO.proAccordion();

        PRO.proToggle();

        PRO.proAlert();

        PRO.proFaq();

        PRO.bsToolTip();

        PRO.wordRotate();

        PRO.widgetTabs();

        PRO.isotopeInitalize();

        PRO.ajaxPagination();

        PRO.ajaxPortfolio();

        PRO.fancybox();

        PRO.onePage();

        PRO.openSearch();

        PRO.footerEffect();

        PRO.proTestimonial();

        PRO.shopTooltip();

        PRO.shopCart();

        PRO.footerSelectMenu();
        PRO.matchHeightVC();

        titleParallax.init();
        parallax.init();
    });

    $(window).scroll(function () {

    });

    $(window).load(function () {

        PRO.loadScreen();

    })

    $(window).resize(function () {

        PRO.dynamicVars();

        PRO.footerEffect();

    });

})(jQuery, window, document);