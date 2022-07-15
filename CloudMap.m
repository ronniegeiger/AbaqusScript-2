%%将坐标分为100份
X1=linspace(min(x),max(x),100);
Y1=linspace(min(y),max(y),100);
[X,Y,F]=griddata(x,y,f,x1,y1,'V4');
pcolor(X,Y,F);
shading interp
colormap(Small_Rainbow);
colorbar
