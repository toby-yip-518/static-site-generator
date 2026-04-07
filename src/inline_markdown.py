from textnode import TextType, TextNode

import re

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue

        splited_node = old_node.text.split(delimiter)

        if len(splited_node) % 2 == 0:
            raise Exception("Closing delimiter not found")

        temp_nodes = []
        for i in range(len(splited_node)):
            if splited_node[i] == "":
                continue

            if i % 2 == 0:
                temp_nodes.append(TextNode(splited_node[i], TextType.TEXT))
            else:
                temp_nodes.append(TextNode(splited_node[i], text_type))
        
        new_nodes.extend(temp_nodes)
    
    return new_nodes
    
def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def split_nodes_image(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue

        extracted_images = extract_markdown_images(old_node.text)

        if len(extracted_images) == 0:
            new_nodes.append(old_node)
            continue

        next_text = old_node.text
        for image in extracted_images:
            image_alt = image[0]
            image_link = image[1]
            splited_text = next_text.split(f"![{image_alt}]({image_link})", 1)

            if splited_text[0] != "":
                new_nodes.append(TextNode(splited_text[0], TextType.TEXT))
                
            new_nodes.append(TextNode(image_alt, TextType.IMAGE, image_link))
            next_text = splited_text[1]
        
        if next_text != "":
            new_nodes.append(TextNode(next_text, TextType.TEXT))
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue

        extracted_links = extract_markdown_links(old_node.text)

        if len(extracted_links) == 0:
            new_nodes.append(old_node)
            continue

        next_text = old_node.text
        for link in extracted_links:
            link_text = link[0]
            link_link = link[1]
            splited_text = next_text.split(f"[{link_text}]({link_link})", 1)

            if splited_text[0] != "":
                new_nodes.append(TextNode(splited_text[0], TextType.TEXT))
                
            new_nodes.append(TextNode(link_text, TextType.LINK, link_link))
            next_text = splited_text[1]
        
        if next_text != "":
            new_nodes.append(TextNode(next_text, TextType.TEXT))
    return new_nodes

def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes