from .internal_types import *
from hash_tex_pkgs import hash_pkgs

class Metadata(KeyNode):
    def __init__(self, target: str):
        """
        Configures the metadata fields for the given build target name.
        """
        super().__init__(None)

        # Keys
        self.name: StrValue = StrValue(target)
        self.root_file: StrValue = StrValue(f"{target}.tex")
        self.output_file: StrValue = StrValue(f"{target}.pdf")

        self.authors: StrArrayValue = StrArrayValue(None)

        # Sub-keys
        self.build = BuildKeyNode(self)
        self.static_site = StaticSiteKeyNode(self)
        self.computed = ComputedKeyNode(self)

# KeyNode definitions 
class BuildKeyNode(KeyNode):
    def __init__(self, parent_node: Metadata):
        super().__init__(parent_node)

        # Keys
        self.requires: StrValue = StrValue(None)
        self.no_latex: BoolValue = BoolValue(None)
        self.prebuild_command: StrValue = StrValue(None)
        self.build_command: StrValue = StrValue(None)
        self.postbuild_command: StrValue = StrValue(None)
        self.miktex_package_file: StrValue = StrValue(None)

class StaticSiteKeyNode(KeyNode):
    def __init__(self, parent_node: Metadata):
        super().__init__(parent_node)

        # Keys
        self.description: StrValue = StrValue(None)
        self.meta_description: StrValue = StrValue(None)
        self.custom_md_file: StrValue = StrValue(None)
        self.document_status: StrValue = StrValue(None)
        self.alias_to: StrValue = StrValue(None)
        self.pdf_viewer: StrValue = StrValue(None)
        self.buttons: GenericArrayValue[ButtonKeyNode] = GenericArrayValue(None)

class ButtonKeyNode(KeyNode):
    def __init__(self, parent_node: StaticSiteKeyNode):
        super().__init__(parent_node)

        # Keys
        self.index: IntValue = IntValue(0)
        self.is_primary: BoolValue = BoolValue(False)
        self.text: StrValue = StrValue(None)
        self.icon: StrValue = StrValue(None)
        self.href: StrValue = StrValue(None)

class ComputedKeyNode(KeyNode):
    def __init__(self, parent_node: Metadata):
        super().__init__(parent_node)

        # Keys
        self.is_alias: BoolComputedValue = BoolComputedValue(self.__is_alias)
        self.is_non_file_target: BoolComputedValue = BoolComputedValue(self.__is_non_file_target)
        self.is_pdf_target: BoolComputedValue = BoolComputedValue(self.__is_pdf_target)
        self.tex_pkg_hash: StrComputedValue = StrComputedValue(self.__tex_pkg_hash)

    def __is_alias(self) -> bool:
        metadata: Metadata = self.parent
        alias_to: StrValue = metadata.static_site.alias_to
        return alias_to.get() is not None
    
    def __is_non_file_target(self) -> bool:
        metadata: Metadata = self.parent
        output_file: StrValue = metadata.output_file
        return output_file.get() == "NON_FILE_TARGET"
    
    def __is_pdf_target(self) -> bool:
        metadata: Metadata = self.parent
        output_file: StrValue = metadata.output_file
        return (output_file.get() is not None and
                output_file.get().endswith(".pdf") and
                not self.__is_non_file_target() and
                not self.__is_alias())
    
    def __tex_pkg_hash(self) -> str:
        metadata: Metadata = self.parent
        if self.__is_non_file_target() or self.__is_alias():
            return "0"
        name: StrValue = metadata.name
        return hash_pkgs(name.get(), False)

