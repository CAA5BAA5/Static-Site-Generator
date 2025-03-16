from textnode import TextType, TextNode

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    if not isinstance(old_nodes, list):
        raise TypeError("old_nodes must be a list")

    count = 1
    new_nodes = []
    for node in old_nodes:
        for segment in node.split(delimiter):
            if count % 2 == 1:
                new_nodes.append(TextNode(segment, TextType.TEXT))
            elif count % 2 == 0:
                new_nodes.append(TextNode(segment, text_type))
            count +=1
    
    return new_nodes