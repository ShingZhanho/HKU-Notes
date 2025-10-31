from .metadata_base_parser import MetadataParserBase
from ..metadata import Metadata, ButtonKeyNode

class MetadataV1Parser(MetadataParserBase):
    """
    Parser for version 1 of the metadata file.
    """
    def __init__(self, metadata_file, build_target):
        """
        Initialize the parser with a metadata file.
        """
        super().__init__(metadata_file, build_target)

    def parse(self) -> Metadata:
        # Top-level keys
        root_file_val = self.json_obj.get("build", {}).get("root_file")
        self.parsed_obj.root_file.set_if(
            root_file_val,
            lambda: root_file_val is not None
        )
        
        output_file_val = self.json_obj.get("build", {}).get("output_file")
        self.parsed_obj.output_file.set_if(
            output_file_val,
            lambda: output_file_val is not None
        )

        # "build" sub-keys
        requires_val = self.json_obj.get("build", {}).get("requires")
        self.parsed_obj.build.requires.set_if(
            requires_val,
            lambda: requires_val is not None
        )
        
        # build.no_latex - default: false
        no_latex_val = self.json_obj.get("build", {}).get("no_latex")
        self.parsed_obj.build.no_latex.set_if_else(
            no_latex_val,
            lambda: no_latex_val is not None,
            False
        )
        
        prebuild_command_val = self.json_obj.get("build", {}).get("prebuild_command")
        self.parsed_obj.build.prebuild_command.set_if(
            prebuild_command_val,
            lambda: prebuild_command_val is not None
        )
        
        # build.build_command - default: computed based on root_file
        build_command_val = self.json_obj.get("build", {}).get("build_command")
        self.parsed_obj.build.build_command.set_if_else(
            build_command_val,
            lambda: build_command_val is not None,
            f"latexmk -pdf -f -interaction=nonstopmode -cd -outdir=. ./{self.parsed_obj.root_file.get()}"
        )
        
        postbuild_command_val = self.json_obj.get("build", {}).get("postbuild_command")
        self.parsed_obj.build.postbuild_command.set_if(
            postbuild_command_val,
            lambda: postbuild_command_val is not None
        )
        
        # build.miktex_package_file - default: "packages.tex"
        miktex_package_file_val = self.json_obj.get("build", {}).get("miktex_package_file")
        self.parsed_obj.build.miktex_package_file.set_if_else(
            miktex_package_file_val,
            lambda: miktex_package_file_val is not None,
            "packages.tex"
        )

        # "static_site" keys
        # static_site.description - default: "-"
        description_val = self.json_obj.get("static_site", {}).get("description")
        self.parsed_obj.static_site.description.set_if_else(
            description_val,
            lambda: description_val is not None,
            "-"
        )
        
        meta_description_val = self.json_obj.get("static_site", {}).get("meta_description")
        self.parsed_obj.static_site.meta_description.set_if(
            meta_description_val,
            lambda: meta_description_val is not None
        )
        
        # static_site.custom_md_file - default: ""
        custom_md_file_val = self.json_obj.get("static_site", {}).get("custom_md_file")
        self.parsed_obj.static_site.custom_md_file.set_if_else(
            custom_md_file_val,
            lambda: custom_md_file_val is not None,
            ""
        )
        
        # static_site.document_status - default: "unk"
        document_status_val = self.json_obj.get("static_site", {}).get("document_status")
        self.parsed_obj.static_site.document_status.set_if_else(
            document_status_val,
            lambda: document_status_val is not None,
            "unk"
        )
        
        alias_to_val = self.json_obj.get("static_site", {}).get("alias_to")
        self.parsed_obj.static_site.alias_to.set_if(
            alias_to_val,
            lambda: alias_to_val is not None
        )
        
        # static_site.pdf_viewer - default: "at_head"
        pdf_viewer_val = self.json_obj.get("static_site", {}).get("pdf_viewer")
        self.parsed_obj.static_site.pdf_viewer.set_if_else(
            pdf_viewer_val,
            lambda: pdf_viewer_val is not None,
            "at_head"
        )

        ### COMPATIBILITY WITH V2 FORMAT ###
        # V2 format no longer uses static_site.primary_button and static_site.secondary_button keys.
        # Instead, an object array static_site.buttons is used to define buttons.
        # Old format primary_button and secondary_button will be converted to buttons array here.
        # NOTE: In V1, if no button configuration is provided, default buttons are created.
        # This maintains backward compatibility with the old format.

        self.parsed_obj.static_site.buttons.set([])

        # "static_site" > "primary_button" keys
        primary_button_obj = self.json_obj.get("static_site", {}).get("primary_button")
        # In V1 format, if primary_button key doesn't exist, we treat it as enabled with defaults
        # If it exists, we check the disabled field
        if primary_button_obj is None:
            # No configuration = create default button
            primary_disabled_val = False
            primary_button_obj = {}
        else:
            primary_disabled_val = primary_button_obj.get("disabled")
        
        # Create button if disabled is not True (i.e., if disabled is False or not present)
        if primary_disabled_val is not True:
            primary_button = ButtonKeyNode(self.parsed_obj.static_site)
            primary_button.is_primary.set(True)
            primary_button.index.set(0)
            primary_text_val = primary_button_obj.get("text")
            primary_icon_val = primary_button_obj.get("icon")
            primary_href_val = primary_button_obj.get("href")
            primary_button.text.set_if_else(
                primary_text_val,
                lambda: primary_text_val is not None,
                "Download"
            )
            primary_button.icon.set_if_else(
                primary_icon_val,
                lambda: primary_icon_val is not None,
                "material-download"
            )
            primary_button.href.set_if_else(
                primary_href_val,
                lambda: primary_href_val is not None,
                f"https://hku.jacobshing.com/files/{self.parsed_obj.name.get()}/{self.parsed_obj.output_file.get()}"
            )
            
            self.parsed_obj.static_site.buttons.append(primary_button)

        # "static_site" > "secondary_button" keys
        secondary_button_obj = self.json_obj.get("static_site", {}).get("secondary_button")
        # In V1 format, if secondary_button key doesn't exist, we treat it as enabled with defaults
        # If it exists, we check the disabled field
        if secondary_button_obj is None:
            # No configuration = create default button
            secondary_disabled_val = False
            secondary_button_obj = {}
        else:
            secondary_disabled_val = secondary_button_obj.get("disabled")
        
        # Create button if disabled is not True (i.e., if disabled is False or not present)
        if secondary_disabled_val is not True:
            secondary_button = ButtonKeyNode(self.parsed_obj.static_site)
            secondary_button.is_primary.set(False)
            secondary_button.index.set(1)
            secondary_text_val = secondary_button_obj.get("text")
            secondary_icon_val = secondary_button_obj.get("icon")
            secondary_href_val = secondary_button_obj.get("href")
            secondary_button.text.set_if_else(
                secondary_text_val,
                lambda: secondary_text_val is not None,
                "View source"
            )
            secondary_button.icon.set_if_else(
                secondary_icon_val,
                lambda: secondary_icon_val is not None,
                "material-github"
            )
            secondary_button.href.set_if_else(
                secondary_href_val,
                lambda: secondary_href_val is not None,
                f"https://github.com/ShingZhanho/HKU-Notes/tree/master/src/{self.parsed_obj.name.get()}"
            )
            
            self.parsed_obj.static_site.buttons.append(secondary_button)

        # "authors" keys - default: ["jacob_shing"]
        authors_val = self.json_obj.get("authors")
        self.parsed_obj.authors.set_if_else(
            authors_val,
            lambda: authors_val is not None,
            ["jacob_shing"]
        )

        return self.parsed_obj
