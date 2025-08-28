class Metadata:
    """
    A class to represent metadata for a build target.
    """
    def __init__(self, build_target):
        """
        Set up the metadata fields.
        The values should be set by the reader, not the user.
        """
        self.name = build_target
        self.root_file = f"{self.name}.tex"
        self.output_file = f"{self.name}.pdf"

        # "build" keys
        self.build__requires = None
        self.build__prebuild_command = None
        self.build__build_command = f"latexmk -pdf -f -interaction=nonstopmode -cd -outdir=. ./{self.root_file}"
        self.build__postbuild_command = None
        self.build__miktex_package_file = "packages.tex"

        # "static_site" keys
        self.static_site__description = None
        self.static_site__custom_md_file = None
        self.static_site__document_status = None
        self.static_site__alias_to = None
        self.static_site__pdf_viewer = "at_head"

        # "static_site" > "primary_button" keys
        self.static_site__primary_button__disabled = False
        self.static_site__primary_button__text = "Download"
        self.static_site__primary_button__icon = "material-download"
        self.static_site__primary_button__href = f"https://shingzhanho.github.io/HKU-Notes/files/{self.name}/{self.output_file}"

        # "static_site" > "secondary_button" keys
        self.static_site__secondary_button__disabled = False
        self.static_site__secondary_button__text = "View source"
        self.static_site__secondary_button__icon = "material-github"
        self.static_site__secondary_button__href = f"https://github.com/ShingZhanho/HKU-Notes/tree/master/src/{self.name}"

        # "authors" keys
        self.authors = []

    # computed keys
    # These keys are computed based on static keys.
    def computed__is_alias(self):
        return self.static_site__alias_to is not None
