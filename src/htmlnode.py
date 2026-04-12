



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
            
        


