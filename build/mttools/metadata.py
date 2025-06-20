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
        self.build__build_command = f"latexmk -pdf -f -interaction=nonstopmode -cd -outdir=. ./src/{self.name}/{self.root_file}"
        self.build__postbuild_command = None
        self.build__miktex_package_file = f"./src/{self.name}/packages.tex"

        # "static_site" keys
        self.static_site__description = None
        self.static_site__custom_md_file = None
        self.static_site__document_status = None
