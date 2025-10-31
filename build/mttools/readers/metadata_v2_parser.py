from .metadata_base_parser import MetadataParserBase
from ..metadata import Metadata, ButtonKeyNode
import jsonschema

class MetadataV2Parser(MetadataParserBase):
    """
    Parser for version 2 of the metadata file.
    """
    def __init__(self, metadata_file, build_target):
        """
        Initialize the parser with a metadata file.
        """
        super().__init__(metadata_file, build_target)
        # Validate JSON against v2 schema
        self.__validate_json(self.json_obj)

    @staticmethod
    def __validate_json(json_obj: dict) -> None:
        """
        Validate the JSON object against the v2 schema.
        """
        SCHEMA_URL = "https://hku.jacobshing.com/statics/schemas/v2.json"
        schema = jsonschema.validators.validator_for({"$schema": SCHEMA_URL}).META_SCHEMA
        jsonschema.validate(instance=json_obj, schema=schema)

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

        # "static_site" > "buttons"
        buttons_val = self.json_obj.get("static_site", {}).get("buttons")
        # if buttons_val is None, create two default buttons
        buttons_dicts: list[dict] = []
        if buttons_val is None:
            buttons_dicts = [
                {
                    "is_primary": True,
                    "text": "Download",
                    "icon": "material-download",
                    "href": f"https://hku.jacobshing.com/files/{self.parsed_obj.name.get()}/{self.parsed_obj.output_file.get()}"
                },
                {
                    "is_primary": False,
                    "text": "View source",
                    "icon": "material-github",
                    "href": f"https://github.com/ShingZhanho/HKU-Notes/tree/master/src/{self.parsed_obj.name.get()}"
                }
            ]
        elif isinstance(buttons_val, list):
            buttons_dicts = buttons_val

        def create_button_node(button_dict: dict) -> ButtonKeyNode:
            button_node = ButtonKeyNode(self.parsed_obj.static_site)
            button_node.index.set_if_else(
                button_dict.get("index"),
                lambda: button_dict.get("index") is not None,
                0
            )
            button_node.is_primary.set_if_else(
                button_dict.get("is_primary"),
                lambda: button_dict.get("is_primary") is not None,
                False
            )
            if not button_dict.get("text"):
                raise ValueError("You must provide 'text' for each button.")
            button_node.text.set(button_dict.get("text"))
            button_node.icon.set(button_dict.get("icon")) # icon can be None
            if not button_dict.get("href"):
                raise ValueError("You must provide 'href' for each button.")
            button_node.href.set(button_dict.get("href"))
            return button_node
        
        button_nodes = [create_button_node(b_dict) for b_dict in buttons_dicts]
        # sort button nodes by index
        button_nodes.sort(key=lambda b: b.index.get())
        self.parsed_obj.static_site.buttons.set(button_nodes)

        # "authors" keys - default: ["jacob_shing"]
        authors_val = self.json_obj.get("authors")
        self.parsed_obj.authors.set_if_else(
            authors_val,
            lambda: authors_val is not None,
            ["jacob_shing"]
        )

        return self.parsed_obj
