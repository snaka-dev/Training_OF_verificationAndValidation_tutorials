# 
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("inputfile", help="input VTP filenname")
parser.add_argument("datatype", help="data type of VTP file:error/magError")
parser.add_argument("casename", help="name of case")
args = parser.parse_args()

#dataType = "error" # "magError"
dataType = args.datatype
####
#FileVTP = './verificationAndValidation/schemes/skewnessCavity/results/Gauss-pointLinear/postProcessing/cuttingPlaneError/constant/zNormal.vtp'
#caseName = 'Gaussian-pointLinear'
caseName = args.casename
screenshotFileName = caseName + "-" + dataType + ".png"
fileVTP = args.inputfile
print()
print(f"data file name      : {fileVTP}")
print(f"data type           : {dataType}")
print(f"Screenshot file name: {screenshotFileName}")
print()
####

# trace generated using paraview version 5.10.0-RC1
import paraview
#paraview.compatibility.major = 5
#paraview.compatibility.minor = 10

#### import the simple module from the paraview
from paraview.simple import *
#### disable automatic camera reset on 'Show'
paraview.simple._DisableFirstRenderCameraReset()

# create a new 'XML PolyData Reader'
zNormalvtp = XMLPolyDataReader(registrationName='zNormal.vtp', FileName=[fileVTP])
zNormalvtp.CellArrayStatus = [ dataType ]

# get active view
renderView1 = GetActiveViewOrCreate('RenderView')

# show data in view
zNormalvtpDisplay = Show(zNormalvtp, renderView1, 'GeometryRepresentation')

# trace defaults for the display properties.
zNormalvtpDisplay.Representation = 'Surface'
zNormalvtpDisplay.ColorArrayName = [None, '']
zNormalvtpDisplay.SelectTCoordArray = 'None'
zNormalvtpDisplay.SelectNormalArray = 'None'
zNormalvtpDisplay.SelectTangentArray = 'None'
zNormalvtpDisplay.OSPRayScaleFunction = 'PiecewiseFunction'
zNormalvtpDisplay.SelectOrientationVectors = 'None'
zNormalvtpDisplay.ScaleFactor = 0.1
zNormalvtpDisplay.SelectScaleArray = 'None'
zNormalvtpDisplay.GlyphType = 'Arrow'
zNormalvtpDisplay.GlyphTableIndexArray = 'None'
zNormalvtpDisplay.GaussianRadius = 0.005
zNormalvtpDisplay.SetScaleArray = [None, '']
zNormalvtpDisplay.ScaleTransferFunction = 'PiecewiseFunction'
zNormalvtpDisplay.OpacityArray = [None, '']
zNormalvtpDisplay.OpacityTransferFunction = 'PiecewiseFunction'
zNormalvtpDisplay.DataAxesGrid = 'GridAxesRepresentation'
zNormalvtpDisplay.PolarAxes = 'PolarAxesRepresentation'

# reset view to fit data
renderView1.ResetCamera(False)

#changing interaction mode based on data extents
renderView1.InteractionMode = '2D'
renderView1.CameraPosition = [0.5, 0.5, 9999.949999999255]
renderView1.CameraFocalPoint = [0.5, 0.5, -0.05000000074505806]

# update the view to ensure updated data information
renderView1.Update()

# Properties modified on renderView1
renderView1.CameraParallelProjection = 1

# Properties modified on renderView1.AxesGrid
renderView1.AxesGrid.Visibility = 1

# set scalar coloring
ColorBy(zNormalvtpDisplay, ('CELLS', dataType) )

# rescale color and/or opacity maps used to include current data range
#zNormalvtpDisplay.RescaleTransferFunctionToDataRange(True, False)
zNormalvtpDisplay.RescaleTransferFunctionToDataRange(False, True)

# show color bar/color legend
zNormalvtpDisplay.SetScalarBarVisibility(renderView1, True)

# get color transfer function/color map for 'error'
LUT1 = GetColorTransferFunction( dataType )
LUT1.RGBPoints = [0.0010074699530377984, 0.231373, 0.298039, 0.752941, 4.850463585287798, 0.865003, 0.865003, 0.865003, 9.699919700622559, 0.705882, 0.0156863, 0.14902]
LUT1.ScalarRangeInitialized = 1.0

# get opacity transfer function/opacity map for 'error'
PWF1 = GetOpacityTransferFunction( dataType )
PWF1.Points = [0.0010074699530377984, 0.0, 0.5, 0.0, 9.699919700622559, 1.0, 0.5, 0.0]
PWF1.ScalarRangeInitialized = 1

# get color legend/bar for errorLUT in view renderView1
LUT1ColorBar = GetScalarBar(LUT1, renderView1)
LUT1ColorBar.Title = dataType
LUT1ColorBar.ComponentTitle = ''

# change scalar bar placement
LUT1ColorBar.WindowLocation = 'Any Location'
LUT1ColorBar.Position = [0.8364928909952607, 0.14716981132075468]


# rescale color and/or opacity maps used to include current data range
#zNormalvtpDisplay.RescaleTransferFunctionToDataRange(True, False)
zNormalvtpDisplay.RescaleTransferFunctionToDataRange(False, True)


# create a new 'Text'
text1 = Text(registrationName='Text1')

# set active source
SetActiveSource(zNormalvtp)

# set active source
SetActiveSource(text1)

# Properties modified on text1
#text1.Text = 'Gauss-linear'
text1.Text = caseName 

# show data in view
text1Display = Show(text1, renderView1, 'TextSourceRepresentation')

# update the view to ensure updated data information
renderView1.Update()

# Properties modified on text1Display
text1Display.WindowLocation = 'Lower Right Corner'

# Properties modified on text1Display
text1Display.FontSize = 24

# get layout
layout1 = GetLayout()

# layout/tab size in pixels
layout1.SetSize(844, 530)

# current camera placement for renderView1
renderView1.InteractionMode = '2D'
renderView1.CameraPosition = [0.49338431204253963, 0.47133201885100534, 9999.949999999255]
renderView1.CameraFocalPoint = [0.49338431204253963, 0.47133201885100534, -0.05000000074505806]
renderView1.CameraParallelScale = 0.584385769575659
renderView1.CameraParallelProjection = 1

# save screenshot
SaveScreenshot(screenshotFileName,  renderView1, ImageResolution=[844, 530])

