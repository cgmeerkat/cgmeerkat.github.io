function trackButtonClick(label) {
    gtag('event', 'click', {
        'event_category': 'button',
        'event_label': label,
    });
}

function trackLinkClick(label) {
    gtag('event', 'click', {
        'event_category': 'link',
        'event_label': label,
    });
}

function trackOtherClick(label) {
    gtag('event', 'click', {
        'event_category': 'misc',
        'event_label': label,
    });
}