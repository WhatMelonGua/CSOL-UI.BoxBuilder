# CSOL-UI.BoxBuilder
This is a plugin for the Creator Mode of CSOL !

This plug-in consists of pure Python code, written for the CSOL creator's UI.Box, which allows you to put down your hands to a certain degree and automatically generate Lua code for pictures.

The principle is to read pictures for analysis and output code according to Lua and CSOL specifications.



Using this plug-in, you can:

1. Import jpeg/jpg/png/bmp, even GIF, and support multiple map imports

2. Optimize the imported images within the software to make them more suitable for the CSOL UI.Box usage limit

3. Quick code generation



After downloading the file, click "main.py" to start (here I imported this in the App folder again for a sense of ceremonies)



It is currently in Chinese, welcome to translate.



The GUI interface is written by the Tkinter library, with a large picture display area on the left and an operation area on the right.



Now on the right:

-"选择图像": Click to import an image file, and the same menu bar "Batch" provides a gif, Multimap import method"



-"起始坐标 x, y": Here you can set which coordinate your picture will be displayed in CSOL, but you can also not write it if you are using Lua code.

By adding the corresponding function to the menu bar Export Settings, you can write it yourself (providing functions such as automatic drawing, animation drawing, etc.)



-"导出尺寸": The upper input box is a width setting, and the lower box is a height to change the size of the picture (Note: When you choose to import multiple images and the sizes vary, this feature will make all the pictures this size)

After the input is completed, the Enter key needs to be pressed to be valid, otherwise it will be treated as preset and will not be processed.



-"UI.Box 变量前缀": If you export a single picture several times, the default variable name of the software will conflict, which can be distinguished by prefix.

Software export is divided into three tables named (prefix you set)+_ CT/_ BT/_ ST corresponds to colors, boxes, and sets



- "减色, 优化图像, 设置": Better for UI.Box drawing because of optimized images. Reducing the color of the picture, changing the color block composition of the picture into a rectangle (suitable for UI.box paving).And '设置' provides some setting thresholds for optimizing the picture.



- "导出代码" generates Lua code from images
