import sys, time
from OCP.STEPCAFControl import STEPCAFControl_Reader
from OCP.TDocStd import TDocStd_Document
from OCP.TCollection import TCollection_ExtendedString, TCollection_AsciiString
from OCP.XCAFDoc import XCAFDoc_DocumentTool
from OCP.BRepMesh import BRepMesh_IncrementalMesh
from OCP.RWGltf import RWGltf_CafWriter
from OCP.OCP.collections import IndexedDataMap_TCollection_AsciiString_TCollection_AsciiString as IDM
from OCP.Message import Message_ProgressRange
from OCP.RWMesh import RWMesh_CoordinateSystem
src, dst, defl = sys.argv[1], sys.argv[2], float(sys.argv[3])
t=time.time()
doc = TDocStd_Document(TCollection_ExtendedString("XmlOcaf"))
r = STEPCAFControl_Reader(); r.SetColorMode(True); r.SetNameMode(True)
assert r.ReadFile(src) == 1
r.Transfer(doc)
print('read', round(time.time()-t,1), flush=True)
shp = r.Reader().OneShape()
BRepMesh_IncrementalMesh(shp, defl, False, 0.5, True)
print('mesh', round(time.time()-t,1), flush=True)
w = RWGltf_CafWriter(TCollection_AsciiString(dst), True)
w.ChangeCoordinateSystemConverter().SetInputLengthUnit(0.001)
w.ChangeCoordinateSystemConverter().SetInputCoordinateSystem(RWMesh_CoordinateSystem.RWMesh_CoordinateSystem_Zup)
w.Perform(doc, IDM(), Message_ProgressRange())
print('write', round(time.time()-t,1), flush=True)
