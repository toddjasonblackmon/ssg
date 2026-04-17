
from functools import reduce

class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError()

    def props_to_html(self):
        if self.props is None:
            return ""

        resp = []
        for k,v in self.props.items():
            resp.append(f'{k}="{v}"')

        return " ".join(resp)

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"



class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

    
    def to_html(self):
        if self.value is None:
            raise ValueError('all leaf nodes must have a value')
        if self.tag is None:
            return self.value
        if self.tag == 'p':
            return '<p>' + self.value + '</p>'
        if self.tag == 'a':
            return f'<a {self.props_to_html()}>{self.value}</a>'
        if self.tag == 'img':
            if not self.props or "src" not in self.props:
                raise ValueError('img nodes must include an image')
            alt_str = f'alt="{self.props["alt"]}" ' if 'alt' in self.props else ''
            return f'<img src="{self.props["src"]}" {alt_str}/>'
        if self.tag == 'b':
            return '<b>' + self.value + '</b>'
        if self.tag == 'code':
            return '<code>' + self.value + '</code>'
        if self.tag == 'i':
            return '<i>' + self.value + '</i>'
        if self.tag == 'span':
            props_str = self.props_to_html()
            props_str = ' ' + props_str if len(props_str) > 0 else ''
            return f'<span{self.props_to_html()}>{self.value}</span>'
        else:
            raise NotImplementedError(f'tag: "{self.tag}" not supported')
            
        
class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)


    def to_html(self):
        if self.tag is None:
            raise ValueError('all parent nodes must have a tag')
        if self.children is None or len(self.children) == 0:
            raise ValueError('all parent nodes must have at least one child node')

        children_to_html = reduce(lambda x,y: x + y.to_html(), self.children, "")

        if self.tag == 'p':
            return '<p>' + children_to_html + '</p>'
        if self.tag == 'div':
            return '<div>' + children_to_html + '</div>'
        if self.tag == 'span':
            return '<span>' + children_to_html + '</span>'
        if self.tag == 'pre':
            return '<pre>' + children_to_html + '</pre>'
        if self.tag in [f"h{x}" for x in range(1,7)]:
            return f'<{self.tag}>' + children_to_html + f'</{self.tag}>'
        else:
            return f'<{self.tag}>' + children_to_html + f'</{self.tag}>'






