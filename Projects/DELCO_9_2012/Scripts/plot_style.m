% Preferred style for plots 

%------------------
% Font properties
%------------------

Font_Name = 'Arial';
Font_Interpreter = 'TeX';
Key_Font_Size   = 12;
Title_Font_Size = 16;
Label_Font_Size = 20;
Text_Font_Size = 16;
Scat_Title_Font_Size = 14;
Scat_Label_Font_Size = 14;

%------------------
% Line properties
%------------------

Line_Width      = 1.5;

%------------------
% Plot properties
%------------------

Plot_Units      = 'inches';
Plot_Width      = 7.0;
Plot_Height     = 3.4;
Plot_X          = 1.2;
Plot_Y          = 0.8;

Scat_Plot_Width      = 4.75;
Scat_Plot_Height     = 4.75;
Scat_Plot_X          = 0.75;
Scat_Plot_Y          = 0.75;
Subtitle_Text_Offset = 0.05;

%------------------
% Paper properties
%------------------

Paper_Units     = 'inches';
Paper_Width     = 9.5;
Paper_Height    = 6.0;
Scat_Paper_Height = 6.0;
Scat_Paper_Width  = 6.0;

Paper_Width_Factor = Paper_Width*1.5;
Legend_Width_Factor = Paper_Width*0.9;

%------------------
% Print properties
%------------------

Figure_Visibility = 'off';
Image_File_Type = '-dpdf';

%------------------
% Set default figure properties
%------------------

set(0,'DefaultAxesUnits',Plot_Units)
set(0,'DefaultAxesPosition',[Plot_X,Plot_Y,Plot_Width,Plot_Height])
set(0,'DefaultTextInterpreter',Font_Interpreter)
set(0,'DefaultTextFontname', 'Arial')
set(0,'DefaultAxesFontName',Font_Name)
set(0,'DefaultLineLineWidth',Line_Width)
set(0,'DefaultAxesFontSize',Label_Font_Size)
set(0,'DefaultTextFontSize',Text_Font_Size)
set(0,'DefaultFigurePaperUnits',Paper_Units);
set(0,'DefaultFigurePaperSize',[Paper_Width Paper_Height]);
set(0,'DefaultFigurePaperPosition',[0 0 Paper_Width Paper_Height]);
% set(0,'DefaultVerticalAlignment',[top]);
% set(0,'DefaultHorizontalAlignment',[center]);
% set(0,'DefaultRotation',60);

%------------------
% Define Colors for Plot Lines
%------------------

red = [.89, .102, .109];
blue = [.216, .494, .721];
green = [.302, .686, .29];
purple = [.596, .306, .639];
orange = [1, 0.498, 0.0];
yellow = [1, 1, .2];
brown = [.651, .337, .157];
pink = [.968, .506, .749];
grey = [.6, .6, .6];

