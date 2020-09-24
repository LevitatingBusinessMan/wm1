from wm1 import socketio, app
import json, os
import lxml.etree

import xml.etree.ElementTree as ET 

@socketio.on("setwksp", namespace="/wscommand")
def setwksp(data):
  if not data:
    socketio.send("No requested workspace", namespace = "/notify")
    return
  wksp = "./workspace/workspaces.xml"
  tree = lxml.etree.parse(wksp)
  parent = tree.xpath(".//name[text()='"+data+"']/..")
  curractive = tree.xpath(".//active[text()='true']/..")
  if not parent:
    socketio.send("Workspace not found", namespace = "/notify")
    return

  if curractive == parent:
    socketio.send("Already using this workspace", namespace = "/notify")
    return
  parent[0][1].text = "true"
  curractive[0][1].text = "false"
  tree.write(wksp, pretty_print=True, xml_declaration=True,   encoding="utf-8")
  socketio.send("Now using workspace " + data + " | Window will refresh to reflect changes", namespace = "/notify")
  socketio.emit("reloadws", namespace = "/wscommand")
  return