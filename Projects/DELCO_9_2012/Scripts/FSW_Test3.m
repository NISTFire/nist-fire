%Test 3 of DELCO Data 

clear all
close all

%------------------
% Set Directory
%------------------

datadir = '../Raw_Data/';

%------------------
% Pull Data From File
%------------------

exp_data_read = importdata([datadir,'FSW_Test_3_092812.csv']); % reads in file into text and data structure
exp_data = exp_data_read.data; % assigning variable name to test data
exp_data_header = exp_data_read.textdata; % assigning variable name to test headers

j=1;
for i=1:10:length(exp_data)
    exp_data_reduced(j,:)=exp_data(i,:);
    j=j+1;
end

%------------------
% Set Save Location for Plots
%------------------

plotdirtemp='../Figures/Temperature/';
plotdirheatflux='../Figures/Heat_Flux/';
plotdirvelocity='../Figures/Velocity/';

%------------------
% Defines Parameters for Plots
%------------------

plot_style 

%------------------
% Define TC Arrays 
%------------------

Num_TC_arrays = 4;
TC_per_array = 8;
TC_array_names = {'FSW3 Eastside Array' 'FSW3 Westside Array' 'FSW3 Hallway Array' 'FSW3 Doorway Array'};
TC_array_names_suppression = {'Suppression FSW3 Eastside Array' 'Suppression FSW3 Westside Array' 'Suppression FSW3 Hallway Array' 'Suppression FSW3 Doorway Array'};
% for j=1:Num_TC_arrays
%     TC_array_suppression = strcat('Suppression ',TC_array_names{j});
% end

TC_array(1,:) = {'Eastside 0.03m' 'Eastside 0.3m' 'Eastside 0.61m' 'Eastside 0.91m' 'Eastside 1.22m' 'Eastside 1.52m' 'Eastside 1.83m' 'Eastside 2.13m'};
TC_array(2,:) = {'Westside 0.03m' 'Westside 0.3m' 'Westside 0.61m' 'Westside 0.91m' 'Westside 1.22m' 'Westside 1.52m' 'Westside 1.83m' 'Westside 2.13m'};
TC_array3(1,:) = {'Hallway 0.3m' 'Hallway 0.61m' 'Hallway 0.91m' 'Hallway 1.22m' 'Hallway 1.52m' 'Hallway 1.83m' 'Hallway 2.13m'};
TC_array4(1,:) = {'Doorway 0.3m' 'Doorway 0.61m' 'Doorway 0.91m' 'Doorway 1.22m' 'Doorway 1.52m' 'Doorway 1.83m'};

%------------------
% Plot TC Arrays Showing Full Tests
%------------------

for j=1:Num_TC_arrays-2
    figure(j)
    hold on
    box on
    plot(exp_data_reduced(:,1),exp_data_reduced(:,8*j-6),'-^','Color',red)      % TC1
    plot(exp_data_reduced(:,1),exp_data_reduced(:,8*j-5),'-+','Color',blue)      % TC2
    plot(exp_data_reduced(:,1),exp_data_reduced(:,8*j-4),'-o','Color',green)      % TC3
    plot(exp_data_reduced(:,1),exp_data_reduced(:,8*j-3),'-.','Color',purple)      % TC4
    plot(exp_data_reduced(:,1),exp_data_reduced(:,8*j-2),'-x','Color',orange)      % TC5
    plot(exp_data_reduced(:,1),exp_data_reduced(:,8*j-1),'-s','Color',grey)      % TC6
    plot(exp_data_reduced(:,1),exp_data_reduced(:,8*j),'-d','Color',brown)        % TC7
    plot(exp_data_reduced(:,1),exp_data_reduced(:,8*j+1),'-v','Color',pink)   % TC8
    line([231;231],[0;1100],'Color','k','LineWidth',1)
    line([254;254],[0;1100],'Color','k','LineWidth',1)
    line([273;273],[0;1100],'Color','k','LineWidth',1)
    line([300;300],[0;1100],'Color','k','LineWidth',1)
    text(241,1275,{'Hallway Nozzle On'},'VerticalAlignment','top','HorizontalAlignment','center','Rotation',60)
    text(264,1275,{'Hallway Nozzle Off'},'VerticalAlignment','top','HorizontalAlignment','center','Rotation',60)
    text(283,1275,{'Room Nozzle On'},'VerticalAlignment','top','HorizontalAlignment','center','Rotation',60)
    text(310,1275,{'Room Nozzle Off'},'VerticalAlignment','top','HorizontalAlignment','center','Rotation',60)
    xlabel('Time (s)')
    ylabel('Temperature ( \circ C)')
    axis([0 350 0 1000])
    legend_handle = legend(TC_array(j,:),'Location','NorthEastOutside');
    pos = get(legend_handle,'position');
    set(legend_handle,'position',[Legend_Width_Factor (Plot_Y+(Plot_Height-pos(4))/2) 3 pos(4)])
    set(gcf,'PaperSize',[Paper_Width_Factor Paper_Height]);
    set(gcf,'PaperPosition',[0 0 Paper_Width*1.5 Paper_Height]);
    plotname = [plotdirtemp TC_array_names{j}];
    print(gcf,'-dpdf',plotname)
    hold off
end

figure(3)
j=3;
hold on
box on
plot(exp_data_reduced(:,1),exp_data_reduced(:,7*j-3),'-^','Color',red)      % TC1
plot(exp_data_reduced(:,1),exp_data_reduced(:,7*j-2),'-+','Color',blue)      % TC2
plot(exp_data_reduced(:,1),exp_data_reduced(:,7*j-1),'-o','Color',green)      % TC3
plot(exp_data_reduced(:,1),exp_data_reduced(:,7*j),'-.','Color',purple)        % TC4
plot(exp_data_reduced(:,1),exp_data_reduced(:,7*j+1),'-x','Color',orange)      % TC5
plot(exp_data_reduced(:,1),exp_data_reduced(:,7*j+2),'-s','Color',grey)        % TC6
plot(exp_data_reduced(:,1),exp_data_reduced(:,7*j+3),'-d','Color',brown)      % TC7
line([231;231],[0;1100],'Color','k','LineWidth',1)
line([254;254],[0;1100],'Color','k','LineWidth',1)
line([273;273],[0;1100],'Color','k','LineWidth',1)
line([300;300],[0;1100],'Color','k','LineWidth',1)
text(241,1275,{'Hallway Nozzle On'},'VerticalAlignment','top','HorizontalAlignment','center','Rotation',60)
text(264,1275,{'Hallway Nozzle Off'},'VerticalAlignment','top','HorizontalAlignment','center','Rotation',60)
text(283,1275,{'Room Nozzle On'},'VerticalAlignment','top','HorizontalAlignment','center','Rotation',60)
text(310,1275,{'Room Nozzle Off'},'VerticalAlignment','top','HorizontalAlignment','center','Rotation',60)
xlabel('Time (s)')
ylabel('Temperature ( \circ C)')
axis([0 350 0 1000])
legend_handle = legend(TC_array3(1,:),'Location','NorthEastOutside');
pos = get(legend_handle,'position');
set(legend_handle,'position',[Legend_Width_Factor (Plot_Y+(Plot_Height-pos(4))/2) 3 pos(4)])
set(gcf,'PaperSize',[Paper_Width_Factor Paper_Height]);
set(gcf,'PaperPosition',[0 0 Paper_Width*1.5 Paper_Height]);
plotname = [plotdirtemp TC_array_names{j}];
print(gcf,'-dpdf',plotname)
hold off

figure(4)
j=4;
hold on
box on
plot(exp_data_reduced(:,1),exp_data_reduced(:,7*j-3),'-^','Color',red)      % TC1
plot(exp_data_reduced(:,1),exp_data_reduced(:,7*j-2),'-+','Color',blue)      % TC2
plot(exp_data_reduced(:,1),exp_data_reduced(:,7*j-1),'-o','Color',green)      % TC3
plot(exp_data_reduced(:,1),exp_data_reduced(:,7*j),'-.','Color',purple)        % TC4
plot(exp_data_reduced(:,1),exp_data_reduced(:,7*j+1),'-x','Color',orange)      % TC5
plot(exp_data_reduced(:,1),exp_data_reduced(:,7*j+2),'-s','Color',grey)      % TC6
plot(exp_data_reduced(:,1),exp_data_reduced(:,7*j+3),'-d','Color',brown)      % TC7
line([231;231],[0;1100],'Color','k','LineWidth',1)
line([254;254],[0;1100],'Color','k','LineWidth',1)
line([273;273],[0;1100],'Color','k','LineWidth',1)
line([300;300],[0;1100],'Color','k','LineWidth',1)
text(241,1275,{'Hallway Nozzle On'},'VerticalAlignment','top','HorizontalAlignment','center','Rotation',60)
text(264,1275,{'Hallway Nozzle Off'},'VerticalAlignment','top','HorizontalAlignment','center','Rotation',60)
text(283,1275,{'Room Nozzle On'},'VerticalAlignment','top','HorizontalAlignment','center','Rotation',60)
text(310,1275,{'Room Nozzle Off'},'VerticalAlignment','top','HorizontalAlignment','center','Rotation',60)
xlabel('Time (s)')
ylabel('Temperature ( \circ C)')
axis([0 350 0 1000])
legend_handle = legend(TC_array4(1,:),'Location','NorthEastOutside');
pos = get(legend_handle,'position');
set(legend_handle,'position',[Legend_Width_Factor (Plot_Y+(Plot_Height-pos(4))/2) 3 pos(4)])
set(gcf,'PaperSize',[Paper_Width_Factor Paper_Height]);
set(gcf,'PaperPosition',[0 0 Paper_Width*1.5 Paper_Height]);
plotname = [plotdirtemp TC_array_names{j}];
print(gcf,'-dpdf',plotname)
hold off



%------------------
% Axis to Show Suppression
%------------------

for j=1:Num_TC_arrays-2
    figure()
    hold on
    box on
    plot(exp_data_reduced(:,1),exp_data_reduced(:,8*j-6),'-^','Color',red)      % TC1
    plot(exp_data_reduced(:,1),exp_data_reduced(:,8*j-5),'-+','Color',blue)      % TC2
    plot(exp_data_reduced(:,1),exp_data_reduced(:,8*j-4),'-o','Color',green)      % TC3
    plot(exp_data_reduced(:,1),exp_data_reduced(:,8*j-3),'-.','Color',purple)      % TC4
    plot(exp_data_reduced(:,1),exp_data_reduced(:,8*j-2),'-x','Color',orange)      % TC5
    plot(exp_data_reduced(:,1),exp_data_reduced(:,8*j-1),'-s','Color',grey)      % TC6
    plot(exp_data_reduced(:,1),exp_data_reduced(:,8*j),'-d','Color',brown)        % TC7
    plot(exp_data_reduced(:,1),exp_data_reduced(:,8*j+1),'-v','Color',pink)   % TC8
    line([231;231],[0;1100],'Color','k','LineWidth',1)
    line([254;254],[0;1100],'Color','k','LineWidth',1)
    line([273;273],[0;1100],'Color','k','LineWidth',1)
    line([300;300],[0;1100],'Color','k','LineWidth',1)
    text(231,1275,{'Hallway Nozzle On'},'VerticalAlignment','top','HorizontalAlignment','center','Rotation',60)
    text(254,1275,{'Hallway Nozzle Off'},'VerticalAlignment','top','HorizontalAlignment','center','Rotation',60)
    text(273,1275,{'Room Nozzle On'},'VerticalAlignment','top','HorizontalAlignment','center','Rotation',60)
    text(300,1275,{'Room Nozzle Off'},'VerticalAlignment','top','HorizontalAlignment','center','Rotation',60)
    xlabel('Time (s)')
    ylabel('Temperature ( \circ C)')
    axis([200 350 0 1000])
    legend_handle = legend(TC_array(j,:),'Location','NorthEastOutside');
    pos = get(legend_handle,'position');
    set(legend_handle,'position',[Legend_Width_Factor (Plot_Y+(Plot_Height-pos(4))/2) 3 pos(4)])
    set(gcf,'PaperSize',[Paper_Width_Factor Paper_Height]);
    set(gcf,'PaperPosition',[0 0 Paper_Width*1.5 Paper_Height]);
    plotname = [plotdirtemp TC_array_names_suppression{j}];
    print(gcf,'-dpdf',plotname)
    hold off
end

figure()
j=3;
hold on
box on
plot(exp_data_reduced(:,1),exp_data_reduced(:,7*j-3),'-^','Color',red)      % TC1
plot(exp_data_reduced(:,1),exp_data_reduced(:,7*j-2),'-+','Color',blue)      % TC2
plot(exp_data_reduced(:,1),exp_data_reduced(:,7*j-1),'-o','Color',green)      % TC3
plot(exp_data_reduced(:,1),exp_data_reduced(:,7*j),'-.','Color',purple)        % TC4
plot(exp_data_reduced(:,1),exp_data_reduced(:,7*j+1),'-x','Color',orange)      % TC5
plot(exp_data_reduced(:,1),exp_data_reduced(:,7*j+2),'-s','Color',grey)        % TC6
plot(exp_data_reduced(:,1),exp_data_reduced(:,7*j+3),'-d','Color',brown)      % TC7
line([231;231],[0;1100],'Color','k','LineWidth',1)
line([254;254],[0;1100],'Color','k','LineWidth',1)
line([273;273],[0;1100],'Color','k','LineWidth',1)
line([300;300],[0;1100],'Color','k','LineWidth',1)
text(231,1275,{'Hallway Nozzle On'},'VerticalAlignment','top','HorizontalAlignment','center','Rotation',60)
text(254,1275,{'Hallway Nozzle Off'},'VerticalAlignment','top','HorizontalAlignment','center','Rotation',60)
text(273,1275,{'Room Nozzle On'},'VerticalAlignment','top','HorizontalAlignment','center','Rotation',60)
text(300,1275,{'Room Nozzle Off'},'VerticalAlignment','top','HorizontalAlignment','center','Rotation',60)
xlabel('Time (s)')
ylabel('Temperature ( \circ C)')
axis([200 350 0 1000])
legend_handle = legend(TC_array3(1,:),'Location','NorthEastOutside');
pos = get(legend_handle,'position');
set(legend_handle,'position',[Legend_Width_Factor (Plot_Y+(Plot_Height-pos(4))/2) 3 pos(4)])
set(gcf,'PaperSize',[Paper_Width_Factor Paper_Height]);
set(gcf,'PaperPosition',[0 0 Paper_Width*1.5 Paper_Height]);
plotname = [plotdirtemp TC_array_names_suppression{j}];
print(gcf,'-dpdf',plotname)
hold off

figure()
j=4;
hold on
box on
plot(exp_data_reduced(:,1),exp_data_reduced(:,7*j-3),'-^','Color',red)      % TC1
plot(exp_data_reduced(:,1),exp_data_reduced(:,7*j-2),'-+','Color',blue)      % TC2
plot(exp_data_reduced(:,1),exp_data_reduced(:,7*j-1),'-o','Color',green)      % TC3
plot(exp_data_reduced(:,1),exp_data_reduced(:,7*j),'-.','Color',purple)        % TC4
plot(exp_data_reduced(:,1),exp_data_reduced(:,7*j+1),'-x','Color',orange)      % TC5
plot(exp_data_reduced(:,1),exp_data_reduced(:,7*j+2),'-s','Color',grey)      % TC6
plot(exp_data_reduced(:,1),exp_data_reduced(:,7*j+3),'-d','Color',brown)      % TC7
line([231;231],[0;1100],'Color','k','LineWidth',1)
line([254;254],[0;1100],'Color','k','LineWidth',1)
line([273;273],[0;1100],'Color','k','LineWidth',1)
line([300;300],[0;1100],'Color','k','LineWidth',1)
text(231,1275,{'Hallway Nozzle On'},'VerticalAlignment','top','HorizontalAlignment','center','Rotation',60)
text(254,1275,{'Hallway Nozzle Off'},'VerticalAlignment','top','HorizontalAlignment','center','Rotation',60)
text(273,1275,{'Room Nozzle On'},'VerticalAlignment','top','HorizontalAlignment','center','Rotation',60)
text(300,1275,{'Room Nozzle Off'},'VerticalAlignment','top','HorizontalAlignment','center','Rotation',60)
xlabel('Time (s)')
ylabel('Temperature ( \circ C)')
axis([200 350 0 1000])
legend_handle = legend(TC_array4(1,:),'Location','NorthEastOutside');
pos = get(legend_handle,'position');
set(legend_handle,'position',[Legend_Width_Factor (Plot_Y+(Plot_Height-pos(4))/2) 3 pos(4)])
set(gcf,'PaperSize',[Paper_Width_Factor Paper_Height]);
set(gcf,'PaperPosition',[0 0 Paper_Width*1.5 Paper_Height]);
plotname = [plotdirtemp TC_array_names_suppression{j}];
print(gcf,'-dpdf',plotname)
hold off

%------------------
% Heat Flux Calculation
%------------------

heat_flux = exp_data(:,47:54);
devc_data = size(heat_flux);
hf_conv_cons = [10.96;12.39;3;-6.242;3.37;2.144;2.203;2.457];

for i = 1:devc_data(2)
    heat_flux_avg(i) = mean(heat_flux(1:31,i));                  % zeroing average for heat flux data
    heat_flux(1,i) = 1000*hf_conv_cons(i)*heat_flux_avg(i);      % setting inital value to zero average
    for j = 2:devc_data(1)
        heat_flux(j,i) = 1000*hf_conv_cons(i)*(heat_flux(j,i) - heat_flux_avg(i));
    end
end

j=1;
for i=1:10:length(heat_flux)
    heat_flux_reduced(j,:)=heat_flux(i,:);
    j=j+1;
end

%------------------
% Heat Flux Plot
%------------------

plot1 = figure;
hold on
box on
plot(exp_data_reduced(:,1),heat_flux_reduced(:,1),'-^','Color',blue) % HF1
plot(exp_data_reduced(:,1),heat_flux_reduced(:,2),'-+','Color',red) % RAD1
line([231;231],[0;1100],'Color','k','LineWidth',1)
line([254;254],[0;1100],'Color','k','LineWidth',1)
line([273;273],[0;1100],'Color','k','LineWidth',1)
line([300;300],[0;1100],'Color','k','LineWidth',1)
text(231,77,{'Hallway Nozzle On'},'VerticalAlignment','top','HorizontalAlignment','center','Rotation',60)
text(254,77,{'Hallway Nozzle Off'},'VerticalAlignment','top','HorizontalAlignment','center','Rotation',60)
text(273,77,{'Room Nozzle On'},'VerticalAlignment','top','HorizontalAlignment','center','Rotation',60)
text(300,77,{'Room Nozzle Off'},'VerticalAlignment','top','HorizontalAlignment','center','Rotation',60)
xlabel('Time (s)')
ylabel('Heat Flux (kW/m^2)')
axis([200 350 0 60])
legend_handle = legend('Eastside Heat Flux 0.15m','Eastside Rad 0.15m','Location','NorthEastOutside');
pos = get(legend_handle,'position');
set(legend_handle,'position',[Legend_Width_Factor (Plot_Y+(Plot_Height-pos(4))/2) 4 pos(4)])
set(gcf,'PaperSize',[Paper_Width_Factor Paper_Height]);
set(gcf,'PaperPosition',[0 0 Paper_Width*1.5 Paper_Height]);
print(gcf,'-dpdf',[plotdirheatflux,'FSW Test 3 Heat Flux Eastside'])
hold off

plot1 = figure;
hold on
box on
plot(exp_data_reduced(:,1),heat_flux_reduced(:,3),'-^','Color',blue) % HF1
plot(exp_data_reduced(:,1),heat_flux_reduced(:,4),'-+','Color',red) % RAD1
line([231;231],[0;1100],'Color','k','LineWidth',1)
line([254;254],[0;1100],'Color','k','LineWidth',1)
line([273;273],[0;1100],'Color','k','LineWidth',1)
line([300;300],[0;1100],'Color','k','LineWidth',1)
text(231,77,{'Hallway Nozzle On'},'VerticalAlignment','top','HorizontalAlignment','center','Rotation',60)
text(254,77,{'Hallway Nozzle Off'},'VerticalAlignment','top','HorizontalAlignment','center','Rotation',60)
text(273,77,{'Room Nozzle On'},'VerticalAlignment','top','HorizontalAlignment','center','Rotation',60)
text(300,77,{'Room Nozzle Off'},'VerticalAlignment','top','HorizontalAlignment','center','Rotation',60)
xlabel('Time (s)')
ylabel('Heat Flux (kW/m^2)')
axis([200 350 0 60])
legend_handle = legend('Westside Heat Flux 0.15m','Westside Rad 0.15m','Location','NorthEastOutside');
pos = get(legend_handle,'position');
set(legend_handle,'position',[Legend_Width_Factor (Plot_Y+(Plot_Height-pos(4))/2) 4 pos(4)])
set(gcf,'PaperSize',[Paper_Width_Factor Paper_Height]);
set(gcf,'PaperPosition',[0 0 Paper_Width*1.5 Paper_Height]);
print(gcf,'-dpdf',[plotdirheatflux,'FSW Test 3 Heat Flux Westside'])
hold off

plot1 = figure;
hold on
box on
plot(exp_data_reduced(:,1),heat_flux_reduced(:,5),'-^','Color',blue) % HF1
plot(exp_data_reduced(:,1),heat_flux_reduced(:,6),'-+','Color',red) % RAD1
line([231;231],[0;1100],'Color','k','LineWidth',1)
line([254;254],[0;1100],'Color','k','LineWidth',1)
line([273;273],[0;1100],'Color','k','LineWidth',1)
line([300;300],[0;1100],'Color','k','LineWidth',1)
text(231,77,{'Hallway Nozzle On'},'VerticalAlignment','top','HorizontalAlignment','center','Rotation',60)
text(254,77,{'Hallway Nozzle Off'},'VerticalAlignment','top','HorizontalAlignment','center','Rotation',60)
text(273,77,{'Room Nozzle On'},'VerticalAlignment','top','HorizontalAlignment','center','Rotation',60)
text(300,77,{'Room Nozzle Off'},'VerticalAlignment','top','HorizontalAlignment','center','Rotation',60)
xlabel('Time (s)')
ylabel('Heat Flux (kW/m^2)')
axis([200 350 0 60])
legend_handle = legend('Hallway Heat Flux 1.52m','Hallway Heat Flux 1.52m','Location','NorthEastOutside');
pos = get(legend_handle,'position');
set(legend_handle,'position',[Legend_Width_Factor (Plot_Y+(Plot_Height-pos(4))/2) 4 pos(4)])
set(gcf,'PaperSize',[Paper_Width_Factor Paper_Height]);
set(gcf,'PaperPosition',[0 0 Paper_Width*1.5 Paper_Height]);
print(gcf,'-dpdf',[plotdirheatflux,'FSW Test 3 Heat Flux Hallway'])
hold off

plot1 = figure;
hold on
box on
plot(exp_data_reduced(:,1),heat_flux_reduced(:,7),'-^','Color',blue) % HF1
plot(exp_data_reduced(:,1),heat_flux_reduced(:,8),'-+','Color',red) % RAD1
line([231;231],[0;1100],'Color','k','LineWidth',1)
line([254;254],[0;1100],'Color','k','LineWidth',1)
line([273;273],[0;1100],'Color','k','LineWidth',1)
line([300;300],[0;1100],'Color','k','LineWidth',1)
text(231,77,{'Hallway Nozzle On'},'VerticalAlignment','top','HorizontalAlignment','center','Rotation',60)
text(254,77,{'Hallway Nozzle Off'},'VerticalAlignment','top','HorizontalAlignment','center','Rotation',60)
text(273,77,{'Room Nozzle On'},'VerticalAlignment','top','HorizontalAlignment','center','Rotation',60)
text(300,77,{'Room Nozzle Off'},'VerticalAlignment','top','HorizontalAlignment','center','Rotation',60)
xlabel('Time (s)')
ylabel('Heat Flux (kW/m^2)')
axis([200 350 0 60])
legend_handle = legend('Near Fire Room Heat Flux 0.15m','Near Fire Room Heat Flux 1.52m','Location','NorthEastOutside');
pos = get(legend_handle,'position');
set(legend_handle,'position',[Legend_Width_Factor (Plot_Y+(Plot_Height-pos(4))/2) 5 pos(4)])
set(gcf,'PaperSize',[Paper_Width_Factor Paper_Height]);
set(gcf,'PaperPosition',[0 0 Paper_Width*1.5 Paper_Height]);
print(gcf,'-dpdf',[plotdirheatflux,'FSW Test 3 Heat Flux Near Fire Room'])
hold off

%------------------
% Bi-Directional Probe Calculation
%------------------

bdp = exp_data(:,33:46);
bdp_zero = bdp(1,:);
bdp_TC = exp_data(:,18:31);
bdp_data = size(bdp);
conv_inch_h2o = 0.4;
conv_pascal = 248.8;

for i = 1:bdp_data(2)
    for j = 1:bdp_data(1)
        pressure(j,i) = conv_inch_h2o*conv_pascal*(bdp(j,i) - bdp_zero(i)); %Converting volatge to pascals 
    end
end

for i = 1:bdp_data(2)
    for j = 1:bdp_data(1)
        velocity(j,i) = 0.0698*sqrt(abs(pressure(j,i))*(bdp_TC(j,i)+273.15))*sign(pressure(j,i)); %Converting pressure to velocities
    end
end

j=1;
for i=1:10:length(velocity)
    velocity_reduced(j,:)=velocity(i,:);
    j=j+1;
end

%------------------
% Define BDP Arrays
%------------------

BDP_array = {'Hallway 0.3m' 'Hallway 0.61m' 'Hallway 0.91m' 'Hallway 1.22m' 'Hallway 1.52m' 'Hallway 1.83m' 'Hallway 1.83m'};
BDP_array2 = {'Doorway 0.15m' 'Doorway 0.3m' 'Doorway 0.61m' 'Doorway 0.91m' 'Doorway 1.22m' 'Doorway 1.52m' 'Doorway 1.83m'};

%------------------
% Bi-Directional Probe Plots
%------------------

plot1 = figure;
hold on
box on
plot(exp_data_reduced(:,1),velocity_reduced(:,1),'-^','Color',red) 
plot(exp_data_reduced(:,1),velocity_reduced(:,2),'-+','Color',blue)
plot(exp_data_reduced(:,1),velocity_reduced(:,3),'-o','Color',green)
plot(exp_data_reduced(:,1),velocity_reduced(:,4),'-.','Color',purple)
plot(exp_data_reduced(:,1),velocity_reduced(:,5),'-x','Color',orange)
plot(exp_data_reduced(:,1),velocity_reduced(:,6),'-s','Color',grey)
plot(exp_data_reduced(:,1),velocity_reduced(:,7),'-d','Color',brown)
line([231;231],[-5;5],'Color','k','Linewidth',1)
line([254;254],[-5;5],'Color','k','Linewidth',1)
line([273;273],[-5;5],'Color','k','Linewidth',1)
line([300;300],[-5;5],'Color','k','Linewidth',1)
text(231,7.75,{'Hallway Nozzle On'},'VerticalAlignment','top','HorizontalAlignment','center','Rotation',60)
text(254,7.75,{'Hallway Nozzle Off'},'VerticalAlignment','top','HorizontalAlignment','center','Rotation',60)
text(273,7.75,{'Room Nozzle On'},'VerticalAlignment','top','HorizontalAlignment','center','Rotation',60)
text(300,7.75,{'Room Nozzle Off'},'VerticalAlignment','top','HorizontalAlignment','center','Rotation',60)
xlabel('Time (s)')
ylabel('Velocity (m/s)')
axis([200 350 -5 5])
legend_handle = legend(BDP_array,'Location','NorthEastOutside');
pos = get(legend_handle,'position');
set(legend_handle,'position',[Legend_Width_Factor (Plot_Y+(Plot_Height-pos(4))/2) 3 pos(4)])
set(gcf,'PaperSize',[Paper_Width_Factor Paper_Height]);
set(gcf,'PaperPosition',[0 0 Paper_Width*1.5 Paper_Height]);
print(gcf,'-dpdf',[plotdirvelocity,'FSW Test 3 Hallway Velocity'])
hold off

plot2 = figure;
hold on
box on
plot(exp_data_reduced(:,1),velocity_reduced(:,8),'-^','Color',red) 
plot(exp_data_reduced(:,1),velocity_reduced(:,9),'-+','Color',blue)
plot(exp_data_reduced(:,1),velocity_reduced(:,10),'-o','Color',green)
plot(exp_data_reduced(:,1),velocity_reduced(:,11),'-.','Color',purple)
plot(exp_data_reduced(:,1),velocity_reduced(:,12),'-x','Color',orange)
plot(exp_data_reduced(:,1),velocity_reduced(:,13),'-s','Color',grey)
plot(exp_data_reduced(:,1),velocity_reduced(:,14),'-d','Color',brown)
line([231;231],[-5;10],'Color','k','Linewidth',1)
line([254;254],[-5;10],'Color','k','Linewidth',1)
line([273;273],[-5;10],'Color','k','Linewidth',1)
line([300;300],[-5;10],'Color','k','Linewidth',1)
text(231,14,{'Hallway Nozzle On'},'VerticalAlignment','top','HorizontalAlignment','center','Rotation',60)
text(254,14,{'Hallway Nozzle Off'},'VerticalAlignment','top','HorizontalAlignment','center','Rotation',60)
text(273,14,{'Room Nozzle On'},'VerticalAlignment','top','HorizontalAlignment','center','Rotation',60)
text(300,14,{'Room Nozzle Off'},'VerticalAlignment','top','HorizontalAlignment','center','Rotation',60)
xlabel('Time (s)')
ylabel('Velocity (m/s)')
axis([200 350 -5 10])
legend_handle = legend(BDP_array2,'Location','NorthEastOutside');
pos = get(legend_handle,'position');
set(legend_handle,'position',[Legend_Width_Factor (Plot_Y+(Plot_Height-pos(4))/2) 3 pos(4)])
set(gcf,'PaperSize',[Paper_Width_Factor Paper_Height]);
set(gcf,'PaperPosition',[0 0 Paper_Width*1.5 Paper_Height]);
print(gcf,'-dpdf',[plotdirvelocity,'FSW Test 3 Doorway Velocity'])
hold off






