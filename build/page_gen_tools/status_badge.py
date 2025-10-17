# Define all the badges in this file
BADGES = {
    # "key": ("description", "icon", "href")
    "sre": (
        "This is a stable release of the document.",
        "material-check-circle",
        "stable-release"
    ),
    "wip": (
        "This document is still under editing and is incomplete.",
        "material-sign-caution",
        "work-in-progress"
    ),
    "lts": (
        "This is a long-term support document.",
        "material-archive-clock",
        "long-term-support"
    ),
    "abd": (
        "This document has been abandoned and may be incomplete. " +
            "It will receive no further updates. It may be removed in the future.",
        "material-cancel",
        "abandoned"
    ),
    "obs": (
        "This document has been reported to be not applicable anymore and is obsolete.",
        "material-clock-alert",
        "obsolete"
    ),
    "fin": (
        "This document is at its final state.",
        "material-calendar-end",
        "final-state"
    ),
    "unk": (
        "The status of this document is unknown.",
        "material-help",
        "unknown-status"
    )
}

def get_badge_str(status_key: str, for_details_page: bool) -> str:
    """
    Returns a one-line string for the badge corresponding to the given status key.
    The href value depends on the for_details_page parameter.
    """
    if status_key not in BADGES:
        raise ValueError(f"Invalid status key: {status_key}")
    description, icon, href_value = BADGES[status_key]
    href = ("../" if for_details_page else "") + f"document-status.md#{href_value}"

    return "".join([
        '<span class="status-badge">',
        f'<span class="status-badge__icon">:{icon}:</span>',
        f'<span class="status-badge__text">[{status_key.upper()}]',
        f'{href} "{description} Click for more info."</span>',
        '</span>'
    ])