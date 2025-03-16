import htmlnode

class ParentNode(htmlnode.HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)
    
    def to_html(self):
        if not self.tag:
            raise ValueError("ParentNode must have a tag")
        if not self.children:
            raise ValueError("ParentNode must have children")
        
        return_value = f"<{self.tag}{self.props_to_html()}>"
        for child in self.children:
            return_value+= child.to_html()
        return_value += f"</{self.tag}>"
        return return_value