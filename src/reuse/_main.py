# SPDX-FileCopyrightText: 2017-2019 Free Software Foundation Europe e.V.
#
# SPDX-License-Identifier: GPL-3.0-or-later

"""Entry functions for reuse."""

import argparse
import logging
import sys
from gettext import gettext as _
from typing import List

from . import (
    __REUSE_version__,
    __version__,
    download,
    header,
    init,
    lint,
    spdx,
)
from ._format import INDENT, fill_all, fill_paragraph
from ._util import setup_logging

_LOGGER = logging.getLogger(__name__)

_DESCRIPTION_LINES = [
    _(
        "reuse is a tool for compliance with the REUSE "
        "recommendations. See <https://reuse.software/> for more "
        "information."
    ),
    _(
        "This version of reuse is compatible with version {} of the REUSE "
        "Specification."
    ).format(__REUSE_version__),
    _("Support the FSFE's work:"),
]

_INDENTED_LINE = _(
    "Donations are critical to our strength and autonomy. They enable us to "
    "continue working for Free Software wherever necessary. Please consider "
    "making a donation at <https://fsfe.org/donate/>."
)

_DESCRIPTION_TEXT = (
    fill_all("\n\n".join(_DESCRIPTION_LINES))
    + "\n\n"
    + fill_paragraph(_INDENTED_LINE, indent_width=INDENT)
)

_EPILOG_TEXT = ""


def parser() -> argparse.ArgumentParser:
    """Create the parser and return it."""
    # pylint: disable=redefined-outer-name
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawTextHelpFormatter,
        description=_DESCRIPTION_TEXT,
        epilog=_EPILOG_TEXT,
    )
    parser.add_argument(
        "--debug", action="store_true", help=_("enable debug statements")
    )
    parser.add_argument(
        "--version",
        action="store_true",
        help=_("show program's version number and exit"),
    )
    parser.set_defaults(func=lambda x, y: parser.print_help())

    subparsers = parser.add_subparsers(title=_("subcommands"))

    add_command(
        subparsers,
        "addheader",
        header.add_arguments,
        header.run,
        help=_("add copyright and licensing into the header of files"),
        description=fill_all(
            _(
                "Add copyright and licensing into the header of one or more "
                "files.\n"
                "\n"
                "By using --copyright and --license, you can specify which "
                "copyright holders and licenses to add to the headers of the "
                "given files.\n"
                "\n"
                "The comment style should be auto-detected for your files. If "
                "a comment style could not be detected, the process aborts. "
                "Use --style to specify or override the comment style to "
                "use.\n"
                # TODO: Remove this
                "\n"
                "IMPORTANT: This is currently EXPERIMENTAL!"
            )
        ),
    )

    add_command(
        subparsers,
        "download",
        download.add_arguments,
        download.run,
        help=_("download a license and place it in the LICENSES/ directory"),
        description=fill_all(
            _(
                "Download a license and place it in the LICENSES/ directory.\n"
                "\n"
                "The LICENSES/ directory is automatically found in the "
                "following order:\n"
                "\n"
                "- The LICENSES/ directory in the root of the VCS "
                "repository.\n"
                "\n"
                "- The current directory if its name is LICENSES.\n"
                "\n"
                "- The LICENSES/ directory in the current directory.\n"
                "\n"
                "If the LICENSES/ directory cannot be found, one is simply "
                "created."
            )
        ),
    )

    add_command(
        subparsers,
        "init",
        init.add_arguments,
        init.run,
        help=_("initialize REUSE project"),
    )

    add_command(
        subparsers,
        "lint",
        lint.add_arguments,
        lint.run,
        help=_("list all non-compliant files"),
        description=fill_all(
            _(
                "Lint the directory or project directory for compliance with "
                "version {reuse_version} of the REUSE Specification. You can "
                "find the latest version of the specification at "
                "<https://reuse.software/spec/>.\n"
                "\n"
                "Specifically, the following criteria are checked:\n"
                "\n"
                "- Are there any bad (unrecognised, not compliant with SPDX) "
                "licenses in the project?\n"
                "\n"
                "- Are any licenses referred to inside of the project, but "
                "not included in the LICENSES/ directory?\n"
                "\n"
                "- Are any licenses included in the LICENSES/ directory that "
                "are not used inside of the project?\n"
                "\n"
                "- Do all files have valid copyright and licensing "
                "information?\n"
            )
        ),
    )

    add_command(
        subparsers,
        "spdx",
        spdx.add_arguments,
        spdx.run,
        help=_("print the project's bill of materials in SPDX format"),
    )

    return parser


def add_command(  # pylint: disable=too-many-arguments
    subparsers,
    name: str,
    add_arguments_func,
    run_func,
    formatter_class=None,
    description: str = None,
    help: str = None,
) -> None:
    """Add a subparser for a command."""
    if formatter_class is None:
        formatter_class = argparse.RawTextHelpFormatter
    subparser = subparsers.add_parser(
        name,
        formatter_class=formatter_class,
        description=description,
        help=help,
    )
    add_arguments_func(subparser)
    subparser.set_defaults(func=run_func)
    subparser.set_defaults(parser=subparser)


def main(args: List[str] = None, out=sys.stdout) -> int:
    """Main entry function."""
    if args is None:
        args = sys.argv[1:]

    main_parser = parser()
    parsed_args = main_parser.parse_args(args)

    setup_logging(
        level=logging.DEBUG if parsed_args.debug else logging.WARNING
    )

    if parsed_args.version:
        out.write("reuse {}\n".format(__version__))
        return 0
    return parsed_args.func(parsed_args, out)


if __name__ == "__main__":
    main()
