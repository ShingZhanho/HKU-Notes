# Document Status

The website displays a ststus badge for each document, indicating its current state.
You may use these badges to help you decide whether this document is suitable for your use.
The statuses that may be displayes are:

## Stable Release

<span class="status-badge">
    <span class="status-badge__icon">
        :material-check-circle:
    </span>
    <span class="status-badge__text">
        [SRE](#stable-release "This is a stable release of the document. Click for more details.")
    </span>
</span>

A stable release indicates that the document is complete and has been through minimum quality checks.
It is suitable for use **during dates not far from the release date**.
A stable release may receive minor updates including typo fixes and formatting changes,
but it will not receive any major updates or content changes.

## Work in Progress

<span class="status-badge">
    <span class="status-badge__icon">
        :material-sign-caution:
    </span>
    <span class="status-badge__text">
        [WIP](#work-in-progress "This document is still under editing and is incomplete. Click for more details.")
    </span>
</span>

A work in progress document is still under editing and is incomplete.
It may contain missing sections, incomplete content, or unverified information.
The contents of the document may change significantly and frequently.
You should not use it for any purposes.

## Long-Term Support

<span class="status-badge">
    <span class="status-badge__icon">
        :material-archive-clock:
    </span>
    <span class="status-badge__text">
        [LTS](#long-term-support "This is a long-term support document. Click for more details.")
    </span>
</span>

A long-term support (LTS) document will only receive updates upon community requests.
It is no longer actively maintained by the author.

## Abandoned

<span class="status-badge">
    <span class="status-badge__icon">
        :material-pencil-off:
    </span>
    <span class="status-badge__text">
        [ABD](#abandoned "This document is no longer being updated and is incomplete. Click for more details.")
    </span>
</span>

An abandoned document is originally a work in progress document. Due to various reasons, it is no longer
being written or updated, and it is incomplete.
It may be removed from the website in the future.

## Obsolete

<span class="status-badge">
    <span class="status-badge__icon">
        :material-clock-alert:
    </span>
    <span class="status-badge__text">
        [OBS](#obsolete "This document is now deprecated. Click for more details.")
    </span>
</span>

This document has been reported by the community to be oudated and no longer applies
to the latest course syllabus. You may still use it for reference with discrepencies expected.

## Unknown Status

<span class="status-badge">
    <span class="status-badge__icon">
        :material-help:
    </span>
    <span class="status-badge__text">
        [UNK](#unknown-status "The status of this document is unknown. Click for more details.")
    </span>
</span>

The document cannot be classified into any of the above categories.
Usually, the details page of the document may provide more information about the document status.
You may also report the status of the document to the website maintainer.

## Error

<span class="status-badge">
    <span class="status-badge__icon">
        :material-alert-octagon:
    </span>
    <span class="status-badge__text">
        [ERR](#error "An error happened during the website generation process. Click for more details.")
    </span>
</span>

This is not a normal status badge. It indicates that an error has occurred during the website generation process.
It can happen when the `metadata.json` file for the document contains invalid values.
If you see this badge, please report it to the website maintainer.