%Test 8 of DELCO Data 

clear all
close all

%------------------
% Set Directory
%------------------

datadir = '../Raw_Data/';

%------------------
% Pull Data From File
%------------------

exp_data_read = importdata([datadir,'FSE_Test_8_093912.csv']); % reads in file into text and data structure
exp_data = exp_data_read.data; % assigning variable name to test data
exp_data_header = exp_data_read.textdata; % assigning variable name to test headers

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
TC_array_names = {'FSE1 Eastside Array' 'FSE1 Westside Array' 'FSE1 Hallway Array' 'FSE1 Doorway Array'};
TC_array_names_suppression = {'Suppression FSE1 Eastside Array' 'Suppression FSE1 Westside Array' 'Suppression FSE1 Hallway Array' 'Suppression FSE1 Doorway Array'};
% for j=1:Num_TC_arrays
%     TC_array_suppression = strcat('Suppression ',TC_array_names{j});
% end

TC_array(1,:) = {'Eastside 0.03m' 'Eastside 0.3m' 'Eastside 0.61m' 'Eastside 0.91m' 'Eastside 1.22m' 'Eastside 1.52m' 'Eastside 1.83m' 'Eastside 2.13m'};
TC_array(2,:) = {'Westside 0.03m' 'Westside 0.3m' 'Westside 0.61m' 'Westside 0.91m' 'Westside 1.22m' 'Westside 1.52m' 'Westside 1.83m' 'Westside 2.13m'};
TC_array3(1,:) = {'Hallway 0.3m' 'Hallway 0.61m' 'Hallway 0.91m' 'Hallway 1.22m' 'Hallway 2.13m'};
TC_array4(1,:) = {'Doorway 0.3m' 'Doorway 0.61m' 'Doorway 0.91m' 'Doorway 1.22m' 'Doorway 1.52m' 'Doorway 1.83m' 'Doorway 2.13m'};

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

%------------------
% Plot TC Arrays Showing Full Tests
%------------------

for j=1:Num_TC_arrays-2
    figure(j)
    hold on
    box on
    plot(exp_data(:,1),exp_data(:,8*j-6),'Color',red)      % TC1
    plot(exp_data(:,1),exp_data(:,8*j-5),'Color',blue)      % TC2
    plot(exp_data(:,1),exp_data(:,8*j-4),'Color',green)      % TC3
    plot(exp_data(:,1),exp_data(:,8*j-3),'Color',purple)      % TC4
    plot(exp_data(:,1),exp_data(:,8*j-2),'Color',orange)      % TC5
    plot(exp_data(:,1),exp_data(:,8*j-1),'Color',grey)      % TC6
    plot(exp_data(:,1),exp_data(:,8*j),'Color',brown)        % TC7
    plot(exp_data(:,1),exp_data(:,8*j+1),'Color',pink)   % TC8
    line([233;233],[0;1100],'Color','k','LineWidth',2)
    line([248;248],[0;1100],'Color','k','LineWidth',2)
    line([269;269],[0;1100],'Color','k','LineWidth',2)
    line([284;284],[0;1100],'Color','k','LineWidth',2)
    text(240,1050,{'Hallway Nozzle On'},'VerticalAlignment','top','HorizontalAlignment','center','FontSize',10,'Rotation',60)
    text(265,1050,{'Hallway Nozzle Off'},'VerticalAlignment','top','HorizontalAlignment','center','FontSize',10,'Rotation',60)
    text(290,1050,{'Room Nozzle On'},'VerticalAlignment','top','HorizontalAlignment','center','FontSize',10,'Rotation',60)
    text(315,1050,{'Room Nozzle Off'},'VerticalAlignment','top','HorizontalAlignment','center','FontSize',10,'Rotation',60)
    xlabel('Time (s)')
    ylabel('Temperature ( \circ C)')
    axis([0 800 0 900])
    legend(TC_array(j,:),'Location','NorthEast')
    plotname = [plotdirtemp TC_array_names{j}];
    print(gcf,'-dpdf',plotname)
    hold off
end

figure(3)
j=3;
hold on
box on
line([233;233],[0;1100],'Color','k')
line([248;248],[0;1100],'Color','k')
line([269;269],[0;1100],'Color','k')
line([284;284],[0;1100],'Color','k')
plot(exp_data(:,1),exp_data(:,7*j-3),'Color','b')      % TC1
plot(exp_data(:,1),exp_data(:,7*j-2),'Color','g')      % TC2
plot(exp_data(:,1),exp_data(:,7*j-1),'Color','r')      % TC3
plot(exp_data(:,1),exp_data(:,7*j),'Color','c')        % TC4
plot(exp_data(:,1),exp_data(:,7*j+3),'Color','k')      % TC7
xlabel('Time (s)')
ylabel('Temperature ( \circ C)')
axis([0 800 0 900])
legend(TC_array3(1,:),'Location','NorthEast')
plotname = [plotdirtemp TC_array_names{j}];
print(gcf,'-dpdf',plotname)
hold off

figure(4)
j=4;
hold on
box on
line([233;233],[0;1100],'Color','k')
line([248;248],[0;1100],'Color','k')
line([269;269],[0;1100],'Color','k')
line([284;284],[0;1100],'Color','k')
plot(exp_data(:,1),exp_data(:,7*j-3),'Color','b')      % TC1
plot(exp_data(:,1),exp_data(:,7*j-2),'Color','g')      % TC2
plot(exp_data(:,1),exp_data(:,7*j-1),'Color','r')      % TC3
plot(exp_data(:,1),exp_data(:,7*j),'Color','c')        % TC4
plot(exp_data(:,1),exp_data(:,7*j+1),'Color','m')      % TC5
plot(exp_data(:,1),exp_data(:,7*j+2),'Color','y')      % TC6
plot(exp_data(:,1),exp_data(:,7*j+3),'Color','k')      % TC7
xlabel('Time (s)')
ylabel('Temperature ( \circ C)')
axis([0 800 0 900])
legend(TC_array4(1,:),'Location','NorthEast')
plotname = [plotdirtemp TC_array_names{j}];
print(gcf,'-dpdf',plotname)
hold off

%------------------
% Axis to Show Suppression
%------------------

for j=1:Num_TC_arrays-2
    figure(j)
    hold on
    box on
    line([233;233],[0;1100],'Color','k')
    line([248;248],[0;1100],'Color','k')
    line([269;269],[0;1100],'Color','k')
    line([284;284],[0;1100],'Color','k')
    plot(exp_data(:,1),exp_data(:,8*j-6),'Color','b')      % TC1
    plot(exp_data(:,1),exp_data(:,8*j-5),'Color','g')      % TC2
    plot(exp_data(:,1),exp_data(:,8*j-4),'Color','r')      % TC3
    plot(exp_data(:,1),exp_data(:,8*j-3),'Color','c')      % TC4
    plot(exp_data(:,1),exp_data(:,8*j-2),'Color','m')      % TC5
    plot(exp_data(:,1),exp_data(:,8*j-1),'Color','y')      % TC6
    plot(exp_data(:,1),exp_data(:,8*j),'Color','k')        % TC7
    xlabel('Time (s)')
    ylabel('Temperature ( \circ C)')
    axis([220 320 0 900])
    legend(TC_array(j,:),'Location','NorthEast')
    plotname = [plotdirtemp TC_array_names_suppression{j}];
    print(gcf,'-dpdf',plotname)
    hold off
end

figure(3)
j=3;
hold on
box on
line([233;233],[0;1100],'Color','k')
line([248;248],[0;1100],'Color','k')
line([269;269],[0;1100],'Color','k')
line([284;284],[0;1100],'Color','k')
plot(exp_data(:,1),exp_data(:,7*j-3),'Color','b')      % TC1
plot(exp_data(:,1),exp_data(:,7*j-2),'Color','g')      % TC2
plot(exp_data(:,1),exp_data(:,7*j-1),'Color','r')      % TC3
plot(exp_data(:,1),exp_data(:,7*j),'Color','c')        % TC4
plot(exp_data(:,1),exp_data(:,7*j+3),'Color','k')      % TC7
xlabel('Time (s)')
ylabel('Temperature ( \circ C)')
axis([220 320 0 900])
legend(TC_array3(1,:),'Location','NorthEast')
plotname = [plotdirtemp TC_array_names_suppression{j}];
print(gcf,'-dpdf',plotname)
hold off

figure(4)
j=4;
hold on
box on
line([233;233],[0;1100],'Color','k')
line([248;248],[0;1100],'Color','k')
line([269;269],[0;1100],'Color','k')
line([284;284],[0;1100],'Color','k')
plot(exp_data(:,1),exp_data(:,7*j-3),'Color','b')      % TC1
plot(exp_data(:,1),exp_data(:,7*j-2),'Color','g')      % TC2
plot(exp_data(:,1),exp_data(:,7*j-1),'Color','r')      % TC3
plot(exp_data(:,1),exp_data(:,7*j),'Color','c')        % TC4
plot(exp_data(:,1),exp_data(:,7*j+1),'Color','m')      % TC5
plot(exp_data(:,1),exp_data(:,7*j+2),'Color','y')      % TC6
plot(exp_data(:,1),exp_data(:,7*j+3),'Color','k')      % TC7
xlabel('Time (s)')
ylabel('Temperature ( \circ C)')
axis([220 320 0 900])
legend(TC_array4(1,:),'Location','NorthEast')
plotname = [plotdirtemp TC_array_names_suppression{j}];
print(gcf,'-dpdf',plotname)
hold off

%------------------
% Heat Flux Calculation
%------------------

heat_flux = exp_data(:,47:54);
devc_data = size(heat_flux);
hf_conv_cons = [11.91;11.35;6.164;6.281;6.375;6.395;5.1975;4.8216];

for i = 1:devc_data(2)
    heat_flux_avg(i) = mean(heat_flux(1:31,i));                  % zeroing average for heat flux data
    heat_flux(1,i) = 1000*hf_conv_cons(i)*heat_flux_avg(i);      % setting inital value to zero average
    for j = 2:devc_data(1)
        heat_flux(j,i) = 1000*hf_conv_cons(i)*(heat_flux(j,i) - heat_flux_avg(i));
    end
end

%------------------
% Heat Flux Plot
%------------------

plot1 = figure;
hold on
box on
line([233;233],[0;1100],'Color','k')
line([248;248],[0;1100],'Color','k')
line([269;269],[0;1100],'Color','k')
line([284;284],[0;1100],'Color','k')
plot(exp_data(:,1),heat_flux(:,1),'Color','b') % HF1
plot(exp_data(:,1),heat_flux(:,2),'Color','r') % RAD1
xlabel('Time (s)')
ylabel('Heat Flux (kW/m^2)')
axis([220 320 0 120])
legend('Heat Flux 0.15m','Rad 0.15m','Location','NorthEast')
print(gcf,'-dpdf',[plotdirheatflux,'FSE Test 1 Heat Flux Eastside'])
hold off

plot1 = figure;
hold on
box on
line([233;233],[0;1100],'Color','k')
line([248;248],[0;1100],'Color','k')
line([269;269],[0;1100],'Color','k')
line([284;284],[0;1100],'Color','k')
plot(exp_data(:,1),heat_flux(:,3),'Color','b') % HF1
plot(exp_data(:,1),heat_flux(:,4),'Color','r') % RAD1
xlabel('Time (s)')
ylabel('Heat Flux (kW/m^2)')
axis([220 320 0 30])
legend('Heat Flux 0.15m','Rad 0.15m','Location','NorthEast')
print(gcf,'-dpdf',[plotdirheatflux,'FSE Test 1 Heat Flux Westside'])
hold off

plot1 = figure;
hold on
box on
line([233;233],[0;1100],'Color','k')
line([248;248],[0;1100],'Color','k')
line([269;269],[0;1100],'Color','k')
line([284;284],[0;1100],'Color','k')
plot(exp_data(:,1),heat_flux(:,5),'Color','b') % HF1
plot(exp_data(:,1),heat_flux(:,6),'Color','r') % RAD1
xlabel('Time (s)')
ylabel('Heat Flux (kW/m^2)')
axis([220 320 0 90])
legend('Heat Flux 0.15m','Rad 0.15m','Location','NorthEast')
print(gcf,'-dpdf',[plotdirheatflux,'FSE Test 1 Heat Flux Hallway'])
hold off

plot1 = figure;
hold on
box on
line([233;233],[0;1100],'Color','k')
line([248;248],[0;1100],'Color','k')
line([269;269],[0;1100],'Color','k')
line([284;284],[0;1100],'Color','k')
plot(exp_data(:,1),heat_flux(:,7),'Color','b') % HF1
plot(exp_data(:,1),heat_flux(:,8),'Color','r') % RAD1
xlabel('Time (s)')
ylabel('Heat Flux (kW/m^2)')
axis([220 320 0 40])
legend('Heat Flux 0.15m','Rad 0.15m','Location','NorthEast')
print(gcf,'-dpdf',[plotdirheatflux,'FSE Test 1 Heat Flux Near Fire Room'])
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

%------------------
% Define BDP Arrays
%------------------

BDP_array = {'Hallway 0.3m' 'Hallway 0.61m' 'Hallway 0.91m' 'Hallway 1.22m' 'Hallway 1.52m' 'Hallway 1.83m' 'Hallway 1.83m'};
BDP_array2 = {'Doorway 0.3m' 'Doorway 0.61m' 'Doorway 0.91m' 'Doorway 1.22m' 'Doorway 1.52m' 'Doorway 1.83m' 'Doorway 2.13m'};

%------------------
% Bi-Directional Probe Plots
%------------------

plot1 = figure;
hold on
box on
line([233;233],[-5;5],'Color','k')
line([248;248],[-5;5],'Color','k')
line([269;269],[-5;5],'Color','k')
line([284;284],[-5;5],'Color','k')
plot(exp_data(:,1),velocity(:,1),'Color','b') 
plot(exp_data(:,1),velocity(:,2),'Color','g')
plot(exp_data(:,1),velocity(:,3),'Color','r')
plot(exp_data(:,1),velocity(:,4),'Color','c')
plot(exp_data(:,1),velocity(:,5),'Color','m')
plot(exp_data(:,1),velocity(:,6),'Color','y')
plot(exp_data(:,1),velocity(:,7),'Color','k')
xlabel('Time (s)')
ylabel('Velocity (m/s)')
axis([200 350 -5 5])
legend(BDP_array,'Location','NorthEast')
print(gcf,'-dpdf',[plotdirvelocity,'FSE Test 1 Hallway Velocity'])
hold off

plot2 = figure;
hold on
box on
line([233;233],[-5;10],'Color','k')
line([248;248],[-5;10],'Color','k')
line([269;269],[-5;10],'Color','k')
line([284;284],[-5;10],'Color','k')
plot(exp_data(:,1),velocity(:,8),'Color','b') 
plot(exp_data(:,1),velocity(:,9),'Color','g')
plot(exp_data(:,1),velocity(:,10),'Color','r')
plot(exp_data(:,1),velocity(:,11),'Color','c')
plot(exp_data(:,1),velocity(:,12),'Color','m')
plot(exp_data(:,1),velocity(:,13),'Color','y')
plot(exp_data(:,1),velocity(:,14),'Color','k')
xlabel('Time (s)')
ylabel('Velocity (m/s)')
axis([200 350 -5 10])
legend(BDP_array2,'Location','NorthEastOutside')
print(gcf,'-dpdf',[plotdirvelocity,'FSE Test 1 Doorway Velocity'])
hold off