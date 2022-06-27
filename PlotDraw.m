%
length_plate=38.0;
width=12.5;
height_plate = 3.0;
spacing_y=0.5;
spacing_x = 0.5;
omega=1.0;
Firstphase_1=0.0;
Firstphase_2=3.0;
incrementstep=0.1;
filename='ArchitectureData.txt';
parameters=[length_plate,width,height_plate,spacing_y,spacing_x,omega,Firstphase_1,Firstphase_2];
%
xarray= [spacing_x/2:incrementstep:length_plate];
yarray= [spacing_y/2:incrementstep:width];
zarray_1=(height_plate/2)*sin(omega*xarray+Firstphase_1)+(height_plate/2);
zarray_2=(height_plate/2)*sin(omega*xarray+Firstphase_2)+(height_plate/2);
plot(xarray,zarray_1,'r',xarray,zarray_2,'-b','LineWidth',1.5,'MarkerSize',10);
print(gcf,'-dpng','Architecture.png');
fileID=fopen(filename,'wt');
fprintf(fileID,'length_plate,width,height_plate,spacing_y,spacing_x,omega,Firstphase_1,Firstphase_2\n');
fprintf(fileID,'%6.1f,%6.1f,%6.1f,%6.1f,%6.1f,%6.1f,%6.1f,%6.1f\n',parameters);
fclose(fileID);