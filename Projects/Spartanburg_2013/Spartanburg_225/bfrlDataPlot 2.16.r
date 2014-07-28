plotdata=function(...){
args=list(...)

createwindow<-function(yheight){
	if(is.na(yheight)&&!is.na(plotHeight)&&!is.na(eventMargin)){ yheight=(plotHeight+eventMargin)/(1-labelMargin) }
	if(is.na(yheight)&&is.na(timeFile)){ yheight=plotHeight }
	#Creating rendering window
	graphics.off()
	if(outputType=="wmf")
		win.metafile(paste(paste(folder,filename, sep=""), "wmf", sep="."),xdim,yheight,12, restoreConsole=FALSE)
	if(outputType=="png")
		png(paste(paste(folder,filename, sep=""), "png", sep="."),xdim,yheight,12, units="in", restoreConsole=FALSE, res=dpi)
	
	return(yheight)
}

axisscale<-function(smax, smin, smult, sscale, maxticks){
	sscale<-10^floor(log(abs(smax-smin))/log(10)-1)
	smult=1
	if(ceiling((smax-smin)/sscale)<maxticks){
	}else if(ceiling((smax-smin)/(2*sscale))<maxticks){
		sscale=2*sscale
		smult=2
	}else if(ceiling((smax-smin)/(3*sscale))<maxticks){
		sscale=3*sscale
		smult=3
	}else if(ceiling((smax-smin)/(5*sscale))<maxticks){
		sscale=5*sscale
		smult=5
	}else if(ceiling((smax-smin)/(10*sscale))<maxticks){
		sscale=10*sscale
		smult=5
	}else if(ceiling((smax-smin)/(20*sscale))<maxticks){
		sscale=20*sscale
		smult=4
	}else if(ceiling((smax-smin)/(30*sscale))<maxticks){
		sscale=30*sscale
		smult=3
	}else{
		sscale=50*sscale
		smult=5
	}
	return(c(smax, smin, smult, sscale, maxticks))
}

remainder<-function(fractional){return(fractional-trunc(fractional))}

eventLocation<-function(xstart, xend, mintheta, toright=NA){
	if(charHeight>eventMargin)
		return(NULL)
	if(xstart==xmin)
		bin=as.vector(subset(timeline, timeline["start"]<=xend&timeline["start"]>=xstart)[["start"]])
	else
		bin=as.vector(subset(timeline, timeline["start"]<=xend&timeline["start"]>xstart)[["start"]])
	if(length(bin)<1)
		return(list())
	theta=atan(charWidth/charHeight)-acos(eventMargin/sqrt(charHeight^2+charWidth^2))
	if(is.nan(theta)){ theta=pi/2 }
	width=charHeight/sin(theta)
	lrr=0
	lrl=0
	if(is.na(toright)){
		if(mean(bin)<(xstart+xend)/2)
			lrl=max(xinch(charWidth*cos(theta)-width*cos(theta)^2-par()[["mai"]][2]),0)
		else
			lrr=max(xinch(charWidth*cos(theta)-width*cos(theta)^2-par()[["mai"]][4]),0)
		total=xinch(width*length(bin))+lrr+lrl
	}else if(toright){
		lrr=max(max(xinch(charWidth*cos(theta)-width*cos(theta)^2)-(xmax-xend),0)-xinch(par()[["mai"]][4]),0)
		total=xinch(width*length(bin))+lrr
	}else if(!toright){
		lrl=max(max(xinch(charWidth*cos(theta)-width*cos(theta)^2)-(xstart-xmin),0)-xinch(par()[["mai"]][2]-width),0)
		total=xinch(width*length(bin))+lrl
	}
	if((xend-xstart)<total&&is.na(toright)&&theta==pi/2){
		cat("   Too many labels.\n")
		return(list(theta=theta, location=xinch(.05)+xstart+seq(0,length(bin)-1)*xinch(width), direction="right"))
	}
	if((xend-xstart)<total)
		return(NULL)
	if(length(bin)<2)
		if(is.na(toright)){
			if(bin[1]>xstart+lrl&bin[1]<xend-lrr-xinch(width)){
				return(list(theta=theta, location=bin[1], direction="right"))
			}else if(bin[1]<xstart+lrl){
				return(list(theta=theta, location=xstart+lrl, direction="right"))
			}else{
				return(list(theta=theta, location=xend-lrr-xinch(width), direction="right"))
			}
		}else if(toright){
			if(bin[1]>xstart+lrl&bin[1]<xend-lrr-xinch(width)){
				return(list(theta=theta, location=bin[1], direction="right"))
			}else if(bin[1]<xstart+lrl){
				return(list(theta=theta, location=xstart+lrl, direction="right"))
			}else{
				return(list(theta=theta, location=xend-lrr-xinch(width), direction="right"))
			}
		}else{
			if(bin[1]>xstart+lrl&bin[1]<xend-lrr-xinch(width)){
				return(list(theta=theta, location=bin[1], direction="left"))
			}else if(bin[1]<xstart+lrl){
				return(list(theta=theta, location=xstart+lrl, direction="left"))
			}else{	
				return(list(theta=theta, location=xend-lrr-xinch(width), direction="left"))
			}
		}
	if(length(bin)>=2){
		if(is.na(toright)){
			binmin=xstart+lrl
			binmax=xend-lrr
		}else if(toright){
			binmin=xstart
			binmax=xend-lrr
		}else{
			binmin=xstart+lrl
			binmax=xend
		}	
		binmean=seq(length(bin)-1)*(binmax-binmin)/length(bin)+binmin
		lmean=binmean-bin[seq(1,length(bin)-1)]
		rmean=binmean-bin[seq(2,length(bin))]
		means=lmean/rmean
		means[means<1&means>0]=1/means[means<1&means>0]
		if(any(means<0)){
			binmean=(binmean[means<0])[which.min(abs(binmean[means<0]-(binmin+binmax)/2))]
		}else{
			binmean=binmean[which.min(means)]
		}
		
		if(is.na(toright)){
			left=eventLocation(xstart, binmean, theta, FALSE)
			right=eventLocation(binmean, xend, theta, TRUE)
		}else if(toright){
			right=eventLocation(binmean, xend, theta, toright)
			left=eventLocation(xstart, binmean, theta, toright)
		}else{
			left=eventLocation(xstart, binmean, theta, toright)
			right=eventLocation(binmean, xend, theta, toright)
		}
	}
	if(is.null(left)||is.null(right)){
		if(is.na(toright))
			if(mean(bin)>(xstart+xend)/2){
				left=eventLocation(xstart, xend, theta, FALSE)
				if(!is.null(left))
					return(list(theta=theta, location=left[["location"]], direction="left"))
				else
					return(list(theta=theta, location=-xinch(.05)+xend-seq(length(bin)-1,0)*xinch(width), direction="left"))
			}else{
				right=eventLocation(xstart, xend, theta, TRUE)
				if(!is.null(right))
					return(list(theta=theta, location=right[["location"]], direction="right"))
				else
					return(list(theta=theta, location=xinch(.05)+xstart+seq(0,length(bin)-1)*xinch(width), direction="right"))					
			}
		else
			if(toright){
				if(mean(bin)<(xstart+xend)/2)
					return(list(theta=theta, location=xstart+seq(0,length(bin)-1)*xinch(width), direction="right"))
				else
					return(list(theta=theta, location=xend-seq(length(bin),1)*xinch(width)-lrr, direction="right"))
			}else{
				if(mean(bin)>(xstart+xend)/2)
					return(list(theta=theta, location=xend-seq(length(bin)-1,0)*xinch(width)-xinch(width), direction="left"))
				else
					return(list(theta=theta, location=xstart+seq(1,length(bin))*xinch(width)-xinch(width)+lrl, direction="left"))
			}
	}
	if(length(left[["location"]])==0&&is.na(toright))
		return(list(theta=theta, location=eventLocation(xstart, xend, theta, FALSE)[["location"]], direction="left"))
	else if(length(right[["location"]])==0&&is.na(toright))
		return(list(theta=theta, location=eventLocation(xstart, xend, theta, TRUE)[["location"]], direction="right"))
	else
		return(list(theta=theta, location=c(left[["location"]], right[["location"]]), direction="split", median=binmean))
}

renderlegend<-function(isMulti,isTop, errorBarX, errorBarY){
	originalsize=legendSize
	originalcols=legendcols
	colors=vector()
	pics=vector()
	colorindex=1
	for(datafile in seq(data)){
		if(length(datafile)!=0)
			for(var in seq(2, dim(data[[datafile]])[2])){
				if(!isMulti||((isTop&&altVars[[datafile]][var-1])||(!isTop&&!altVars[[datafile]][var-1]))){
					colors=append(colors, hsv(h=remainder(1+primary-bandwidth/2+seq(0,totalvars-1)/(max(totalvars-1,1))*bandwidth), s=.85, v=.85)[colorindex])
					pics=append(pics, seq(0, totalvars)[colorindex])
				}
				colorindex=colorindex+1
			}
	}
	if(totalvars>1){
	names=vector()
	n=1
	if(isTop&&isMulti){
		tempymin=altymin
		tempymax=altymax
	}else{
		tempymin=ymin
		tempymax=ymax
	}
	for(file in data){
		visiblevars=!isMulti|((isTop&altVars[[n]])|(!isTop&!altVars[[n]]))
		namelist=dimnames(data[[n]])[[2]][seq(2, dim(as.matrix(dimnames(data[[n]])[[2]]))[1])]
		for(i in seq(length(namelist))){
			if(visiblevars[i])
				if(length(fileSuffix)<n||length(fileSuffix[n])<i&&!suppNames){	
					names=append(names, namelist[i])
				}else if(suppNames){
					names=append(names, fileSuffix[n])
				}else{
					names=append(names, paste(fileSuffix[n], namelist[i], sep="_"))
				}
		}
		n=n+1
	}
	names=chartr("_"," ",names)
	if(is.na(title)||title=="")
		title=NULL
	if(is.na(legendPos)){
	legenddata=legend(x=xmax/2, y=tempymax/2, names, lwd=1, col=colors[seq(dim(reduxdata)[2]-1)], bg=bgcolor, pch=seq(0, totalvars), ncol=legendcols, plot=FALSE, title=title, pt.cex=1, cex=legendSize)
	curMinX=xmin+xinch(.00)+legenddata[[1]][[1]]/2*(1+.05)
	curMinY=tempymin+yinch(.00)+legenddata[[1]][[2]]/2*(1+.05)
	curMaxX=xmax-xinch(.00)-legenddata[[1]][[1]]/2*(1+.05)
	curMaxY=tempymax-yinch(.00)-legenddata[[1]][[2]]/2*(1+.05)
	divides=4
	maxdist=-10000
	lwidth=legenddata[[1]][[1]]*(1/xinch(1))
	lheight=legenddata[[1]][[2]]*(1/yinch(1))
	distance=100000
	increment=divides
	while(increment<=32){
		hasChanged=FALSE
		if(curMinX<curMaxX){
			i=1
			while(i<=increment){
				j=1
				xloc=(curMinX+(curMaxX-curMinX)*(i-.5)/increment)
				while(j<=increment){
					yloc=(curMinY+(curMaxY-curMinY)*(j-.5)/increment)
					ex=(c(errorBarX, errorBarX)-xloc)*(1/xinch(1))
					ey=(c(errorBarY*(1-singleErrorPercent), errorBarY*(1+singleErrorPercent))-yloc)*(1/yinch(1))
					distance=min((sqrt((ex)^2+(ey)^2)-sqrt((lwidth/2)^2+(lwidth/2*ey/ex)^2))[abs(ex/ey)>lwidth/lheight])
					distance=min(distance, min((sqrt((ex)^2+(ey)^2)-sqrt((lheight/2*ex/ey)^2+(lheight/2)^2))[abs(ex/ey)<=lwidth/lheight]))
					n=1
					for(reduxdata in data){
						if(length(reduxdata)==0)
							next
						if(!isMulti|((isTop&altVars[[n]])|(!isTop&!altVars[[n]]))){
							dx=((reduxdata[seq(dim(reduxdata)[1])]-xloc)*(1/xinch(1)))
							dy=matrix((reduxdata[seq(dim(reduxdata)[1]), seq(2, dim(reduxdata)[2])]-yloc)*(1/yinch(1)))
							distance=min(distance, min((sqrt((dx)^2+(dy)^2)-sqrt((lwidth/2)^2+(lwidth/2*dy/dx)^2))[abs(dx/dy)>lwidth/lheight]))
							distance=min(distance, min((sqrt((dx)^2+(dy)^2)-sqrt((lheight/2*dx/dy)^2+(lheight/2)^2))[abs(dx/dy)<=lwidth/lheight]))
						}
						n=n+1
					}
					if(distance>=maxdist||!hasChanged){
						maxdist=distance
						boxX1=(curMinX+(curMaxX-curMinX)*(i-1)/increment)
						boxY1=(curMinY+(curMaxY-curMinY)*(j-1)/increment)
						boxX2=(curMinX+(curMaxX-curMinX)*(i)/increment)
						boxY2=(curMinY+(curMaxY-curMinY)*(j)/increment)
						hasChanged=TRUE
					}
					j=j+1
				}
				i=i+1
			}
			increment=max(2,trunc(increment/2))
			curMinX=boxX1
			curMinY=boxY1
			curMaxX=boxX2
			curMaxY=boxY2
		}else{
			divides=1000
		}
		if((curMaxX-curMinX)<(xmax-xmin)/(10*xdim)&&(curMaxY-curMinY)<(tempymax-tempymin)/(10*ydim)){
			if(maxdist>0){
				cat("   Legend position within accuracy\n")
				increment=1000
			}else{
				cat("   Empty legend position not found, increasing search\n")
				legenddata=legend(x=xmax/2, y=tempymax/2, names, lwd=1, col=colors[seq(dim(reduxdata)[2]-1)], bg=bgcolor, pch=seq(0, totalvars), ncol=legendcols, plot=FALSE, title=title, pt.cex=1)
				divides=divides*2
				increment=divides
				curMinX=xmin+legenddata[[1]][[1]]/2*(1+.05)
				curMinY=tempymin+legenddata[[1]][[2]]/2*(1+.05)
				curMaxX=xmax-legenddata[[1]][[1]]/2*(1+.05)
				curMaxY=tempymax-legenddata[[1]][[2]]/2*(1+.05)
			}
		}
		if(divides>32&&legendcols<3){
			cat("   No space available, switching columns\n")
			divides=4
			increment=divides
			legendcols=legendcols+1
			legenddata=legend(x=xmax/2, y=tempymax/2, names, lwd=1, col=colors[seq(dim(reduxdata)[2]-1)], bg=bgcolor, pch=seq(0, totalvars), ncol=legendcols, plot=FALSE, title=title, pt.cex=1, cex=legendSize)
			curMinX=xmin+legenddata[[1]][[1]]/2*(1+.05)
			curMinY=tempymin+legenddata[[1]][[2]]/2*(1+.05)
			curMaxX=xmax-legenddata[[1]][[1]]/2*(1+.05)
			curMaxY=tempymax-legenddata[[1]][[2]]/2*(1+.05)
			lwidth=legenddata[[1]][[1]]*(1/xinch(1))
			lheight=legenddata[[1]][[2]]*(1/yinch(1))

		}else if(divides>32&&legendSize>1/3){
			cat("   No space available, shrinking legend\n")
			divides=4
			increment=divides
			legendcols=originalcols
			legendSize=legendSize*.75
			legenddata=legend(x=xmax/2, y=tempymax/2, names, lwd=1, col=colors[seq(dim(reduxdata)[2]-1)], bg=bgcolor, pch=seq(0, totalvars), ncol=legendcols, plot=FALSE, title=title, pt.cex=1, cex=legendSize)
			curMinX=xmin+legenddata[[1]][[1]]/2*(1+.05)
			curMinY=tempymin+legenddata[[1]][[2]]/2*(1+.05)
			curMaxX=xmax-legenddata[[1]][[1]]/2*(1+.05)
			curMaxY=tempymax-legenddata[[1]][[2]]/2*(1+.05)
			lwidth=legenddata[[1]][[1]]*(1/xinch(1))
			lheight=legenddata[[1]][[2]]*(1/yinch(1))
		}
	}
	xalign=.5
	yalign=.5
	legendx=(boxX1+(boxX2-boxX1)/2)
	legendy=(boxY1+(boxY2-boxY1)/2)
	if(order){
		tempnames=names[length(names):1]
		temppics=pics[length(pics):1]
		tempcolors=colors[length(colors):1]
	}else{
		tempnames=names
		temppics=pics
		tempcolors=colors
	}
	if(symbols==0){
		legend(x=legendx, y=legendy, tempnames, lty=1, lwd=lineWidth, col=tempcolors, bg=hsv(1,0,1, alpha=.5), xjust=xalign, yjust=yalign, cex=legendSize, text.col=framecolor, ncol=legendcols, bty="o", title=title, pt.cex=1, pt.lwd=lineWidth, box.col=hsv(1,1,0, alpha=.15), box.lwd=lineWidth)
	}else{
		legend(x=legendx, y=legendy, tempnames, lty=0, col=tempcolors, bg=hsv(1,0,1, alpha=.5), pch=temppics, xjust=xalign, yjust=yalign, cex=legendSize, text.col=framecolor, ncol=legendcols, bty="o", title=title, pt.cex=1, pt.lwd=lineWidth, box.col=hsv(1,1,0, alpha=.15), box.lwd=lineWidth)
		if(pointAccent){
			legend(x=legendx, y=legendy, tempnames, lty=0, col="black", bg=hsv(1,0,1, alpha=.5), pch=temppics, xjust=xalign, yjust=yalign, cex=legendSize, text.col=framecolor, ncol=legendcols, bty="n", title=title, pt.cex=1, pt.lwd=lineWidth/2)
		}
	}	
	}else{
		legend(x=legendPos[1], y=legendPos[2], tempnames, lwd=0, col=tempcolors, bg=bgcolor, pch=temppics, cex=legendSize, text.col=framecolor, ncol=legendcols, bty="o", title=title, pt.cex=1)
	}
	}
}

renderaxes<-function(isMulti, isTop){

	if(!isTop||!isMulti)
		mtext(xaxis, side=1, line=1.5, font=2, col=framecolor)
	if(!isTop||!isMulti)
		axis(side=1, las=1, tck=.0125, at=seq(xmin, xmax, xscale), mgp=c(3,.5,0), col=framecolor, col.axis=framecolor, lend=endtype, lwd=lineWidth)
	else
		axis(side=1, las=1, tck=.0125, at=seq(xmin, xmax, xscale), mgp=c(3,.5,0), labels=FALSE, col=framecolor, col.axis=framecolor, lend=endtype, lwd=lineWidth)
	axis(side=1, las=1, tck=.0075, at=seq(xmin, xmax, xscale/xmult), mgp=c(3,.5,0), labels=FALSE, col=framecolor, lend=endtype, lwd=lineWidth)	
	if(isMulti)
		if(!isTop)
			axis(side=2, las=1, tck=.0125, at=seq(ymin, ymax, yscale), mgp=c(3,.5,0), col=framecolor, col.axis=framecolor, lend=endtype, lwd=lineWidth)
		else
			axis(side=2, las=1, tck=.0125, at=seq(altymin, altymax, altyscale), mgp=c(3,.5,0), col=framecolor, col.axis=framecolor, lend=endtype, lwd=lineWidth)
	else
		axis(side=2, las=1, tck=.0125, at=seq(ymin, ymax, yscale), mgp=c(3,.5,0), col=framecolor, col.axis=framecolor, lend=endtype, lwd=lineWidth)
	if(isMulti&&isTop)
		axis(side=2, las=1, tck=.005, at=seq(altymin, altymax, altyscale/altymult), mgp=c(3,.5,0), labels=FALSE, col=framecolor, lend=endtype, lwd=lineWidth)
	else
		axis(side=2, las=1, tck=.005, at=seq(ymin, ymax, yscale/ymult), mgp=c(3,.5,0), labels=FALSE, col=framecolor, lend=endtype, lwd=lineWidth)
	
	if(!is.na(axis2a)&&!is.na(axis2b)&&!is.na(axis2lab)){
		altAxisNew=round(seq(ymin*axis2a+axis2b, ymax*axis2a+axis2b, (ymax-ymin)*axis2a/yticks)/min(c(yscale*100,1)))*min(c(yscale*100,1))
		altAxisOld=seq(ymin, ymax, (ymax-ymin)/yticks)
		axis(side=4, at=altAxisOld, labels=altAxisNew, mgp=c(3,.5,0), tck=.01, las=1, yaxs="i", col=framecolor, col.axis=framecolor, lend=endtype, lwd=lineWidth)
		mtext(axis2lab, side=4, line=2.5, font=2, col=framecolor)
	}
}

renderpoints<-function(isMulti, isTop, isSymbols){
	n=1
	for(filetable in seq(data)){
		reduxdata=data[[filetable]]
		if(length(reduxdata)==0)
			next
		for(var in seq(2,dim(reduxdata)[2])){
			if(!isMulti||((altVars[[filetable]][var-1]&&isTop)||(!altVars[[filetable]][var-1]&&!isTop))){
				if(!isSymbols){
					if(drawLine[filetable])
						points(reduxdata[seq(dim(reduxdata)[1]),1], reduxdata[seq(dim(reduxdata)[1]),var], type="l", col=hsv(h=remainder(1+primary-bandwidth/2+seq(0,totalvars-1)/(max(totalvars-1,1))*bandwidth), s=.85, v=.85)[n], lwd=lineWidth)
					else
						points(reduxdata[seq(dim(reduxdata)[1]),1], reduxdata[seq(dim(reduxdata)[1]),var], type="p", col=hsv(h=remainder(1+primary-bandwidth/2+seq(0,totalvars-1)/(max(totalvars-1,1))*bandwidth), s=.85, v=.85)[n], pch=46, cex=lineWidth)
				}else{
					points(reduxdata[seq(0, dim(data.matrix(reduxdata[seq(dim(reduxdata)[1])]))[1], dim(data.matrix(reduxdata[seq(dim(reduxdata)[1])]))[1]/symbols),1],
						reduxdata[seq(0, dim(data.matrix(reduxdata[seq(dim(reduxdata)[1])]))[1], dim(data.matrix(reduxdata[seq(dim(reduxdata)[1])]))[1]/symbols),var],
						type="p", col=hsv(h=remainder(1+primary-bandwidth/2+seq(0,totalvars-1)/(max(totalvars-1,1))*bandwidth), s=.85, v=.85)[n], pch=n-1, lwd=lineWidth)
					if(pointAccent){
						points(reduxdata[seq(0, dim(data.matrix(reduxdata[seq(dim(reduxdata)[1])]))[1], dim(data.matrix(reduxdata[seq(dim(reduxdata)[1])]))[1]/symbols),1],
							reduxdata[seq(0, dim(data.matrix(reduxdata[seq(dim(reduxdata)[1])]))[1], dim(data.matrix(reduxdata[seq(dim(reduxdata)[1])]))[1]/symbols),var],
							type="p", col="black", pch=n-1, lwd=lineWidth/2)	
					}
				}
			}
			n=n+1
		}
	}
}

rendererrorbar<-function(isMulti, isTop){
	boxX1=0
	boxX2=0
	boxY1=0
	boxY2=0

	if(singleErrorPercent!=0){
		
		barwidth=.13
		if(singleErrorPercent==0){ barwidth=0 }
		datafile=1
		newMax=1
		lastMax=NULL
		while(datafile<=length(data)){
			usedVars=!isMulti|((isTop&altVars[[ datafile ]])|(!isTop&!altVars[[ datafile ]]))
			if(any(usedVars)){
				barwindow=subset(data[[datafile]], data[[datafile]][seq(dim(data.matrix(data[[datafile]]))[1])]<(xmax-(xmax-xmin)*.05)&data[[datafile]][seq(dim(data.matrix(data[[datafile]]))[1])]>(xmin+(xmax-xmin)*.05))
				barwindow=barwindow[seq(dim(barwindow)[1]), c( TRUE, usedVars ) ]
				var=2
				while(var<=dim(barwindow)[2]){
					newMax=which.max(abs(barwindow[seq(dim(barwindow)[1]), var]))
					if(is.null(lastMax)){
						lastMax=barwindow[newMax, var]
						errorBarY=as.vector(barwindow[newMax, var])
						errorBarX=as.vector(barwindow[newMax, 1])
					}
					if(abs(barwindow[newMax, var])>abs(lastMax)){
						lastMax=barwindow[newMax, var]
						errorBarY=as.vector(barwindow[newMax, var])
						errorBarX=as.vector(barwindow[newMax, 1])
					}
					var=var+1
				}
			}
			datafile=datafile+1
		}
		lines(x=c(errorBarX,errorBarX), y=c((1-singleErrorPercent)*errorBarY, (1+singleErrorPercent)*errorBarY), lend=endtype, xpd=NA, lwd=lineWidth)
		lines(x=c(errorBarX-xinch(barwidth),errorBarX+xinch(barwidth)), y=c((1-singleErrorPercent)*errorBarY, (1-singleErrorPercent)*errorBarY), lend=endtype, xpd=NA, lwd=lineWidth)
		lines(x=c(errorBarX-xinch(barwidth),errorBarX+xinch(barwidth)), y=c((1+singleErrorPercent)*errorBarY, (1+singleErrorPercent)*errorBarY), lend=endtype, xpd=NA, lwd=lineWidth)
		lines(x=c(errorBarX-xinch(barwidth)/2,errorBarX+xinch(barwidth)/2), y=c(errorBarY, errorBarY), lend=endtype, xpd=NA, lwd=lineWidth)
	}
	return(list(errorBarX, errorBarY))
}

rendertimeline<-function(isMulti){
	#Rendering timeline data
	offsetsize=(labelMargin*ydim-.04)/(max(overlap)+1)
	if(isMulti){
		ymaxtemp=altymax
		ymintemp=altymin
	}else{
		ymaxtemp=ymax
		ymintemp=ymin
	}
	y1=ymintemp
	y2=ymaxtemp
	y4=ymaxtemp+yinch(labelMargin*ydim)
	for(n in seq(length(eventLocs[["location"]]))){	
		y3=ymaxtemp+yinch(offsetsize*overlap[n])
		x1=data.matrix(timeline["start"])[n]
		x3=eventLocs[["location"]][n]
		if(!any(names(timeline)=="end")||singleEvents){
			lines(x=c(x1, x1), y=c(y2, y3), xpd=NA, col=hsv(1,0, eventcolorlow+(eventcolorhi-eventcolorlow)*n/length(eventLocs[["location"]])), lwd=lineWidth)
			lines(x=c(x1, x3), y=c(y3, y4), xpd=NA, col=hsv(1,0, eventcolorlow+(eventcolorhi-eventcolorlow)*n/length(eventLocs[["location"]])), lwd=lineWidth)
		}else{
			x2=data.matrix(timeline["end"])[n]
			if(x3>x2){
				polygon(x=c(x1, x1, x2, x3, x2,x2), y=c(y1, y3, (x2-x3)*(y3-y4)/(x1-x3)+y4, y4, (x2-x3)*(y3-y4)/(x1-x3)+y4, y1), col=eventcolor, xpd=NA, border=eventcolor)
			}else if(x3<x1){
				polygon(x=c(x1, x1, x3, x1, x2,x2), y=c(y1, (x1-x3)*(y3-y4)/(x2-x3)+y4, y4, (x1-x3)*(y3-y4)/(x2-x3)+y4, y3, y1), col=eventcolor, xpd=NA, border=eventcolor)
			}else{
				polygon(x=c(x1, x1, x3, x2, x2), y=c(y1, y3, y4, y3, y1), col=eventcolor, xpd=NA, border=eventcolor)
			}
		}
		if(length(eventLocs[["location"]])==1)
			angle=0
		else
			angle=eventLocs[["theta"]]*180/pi
		if((eventLocs[["location"]][n]>=eventLocs[["median"]]&&eventLocs[["direction"]]=="split")||eventLocs[["direction"]]=="right"||eventLocs[["theta"]]==pi/2){
			text(x=eventLocs[["location"]][n], y=ymaxtemp+yinch(labelMargin*ydim+.03), timeline[n, "event"], xpd=NA, srt=angle, adj=c(0,0), col=framecolor)
		}else{
			text(x=eventLocs[["location"]][n], y=ymaxtemp+yinch(labelMargin*ydim+.03), timeline[n, "event"], xpd=NA, srt=angle, adj=c(0,0), col=framecolor)
		}
	}
}

renderablines<-function(isMulti, isTop){
	#Rendering timeline data
	offsetsize=(labelMargin*ydim-.04)/(max(overlap)+1)
	if(isMulti&&isTop){
		ymaxtemp=altymax
		ymintemp=altymin
	}else{
		ymaxtemp=ymax
		ymintemp=ymin
	}
	y1=ymintemp
	y2=ymaxtemp
	for(n in seq(length(eventLocs[["location"]]))){	
		x1=data.matrix(timeline["start"])[n]
		if(!any(names(timeline)=="end")||singleEvents){
			abline(v=x1, col=hsv(1,0, eventcolorlow+(eventcolorhi-eventcolorlow)*n/length(eventLocs[["location"]])), lwd=lineWidth)
			if(isMulti&&!isTop){
				lines(x=c(x1, x1), y=c(y2, y2+yinch(mpMedian*ydim)), xpd=NA, col=hsv(1,0,eventcolorlow+(eventcolorhi-eventcolorlow)*n/length(eventLocs[["location"]])), lwd=lineWidth)
			}
			if(!is.na(arrowsize))
				polygon(x=c(x1, x1+xinch(arrowsize/2), x1-xinch(arrowsize/2), x1), y=c(y1, y1+yinch(arrowsize*.866), y1+yinch(arrowsize*.866), y1), xpd=NA, col="white", lwd=lineWidth, border=hsv(1,0,eventcolorlow+(eventcolorhi-eventcolorlow)*n/length(eventLocs[["location"]])))
		}else{
			x2=data.matrix(timeline["end"])[n]
			polygon(x=c(x1, x1, x2, x2), y=c(y1, y2, y2, y1), col=eventcolor, xpd=NA, border=eventcolor)
		}
	}
}



renderplotspace<-function(isMulti, isTop){
	#Sizing the figure region
	tfMar=1
	tfFig=1
	axMar=2
	tpFig=0
	tpMar=3

	if(!is.na(timeFile)){
		tfMar=0
		tfFig=1-eventMargin/ydim-labelMargin
	}
	if(isMulti)
		if(isTop){
			tpFig=tfFig/2+.50/ydim/2+mpMedian/2
			tpMar=0
		}else
			tfFig=tfFig/2+.50/ydim/2-mpMedian/2
	if(!is.na(axis2a)&&!is.na(axis2b)&&!is.na(axis2lab))
		axMar=4
	if(!is.na(customaxis))
		axMar=customAxisMargin
	par(fig=c(0,1, tpFig, tfFig), bg=bgcolor, mar=c(tpMar,4,tfMar,axMar)+.01)
	
	#Rendering the scatter plot
	if(isTop)
		par(new=TRUE)
	if(isMulti&&isTop){
		plot.default(NULL, type="l", ylab=NA, xlim = c(xmin,xmax), ylim = c(altymin,altymax), axes=FALSE, 
			frame.plot=FALSE, las=1, tck=.01, mgp=c(3,.5,0), xaxs="i", yaxs="i", font=2)
	}else
		plot.default(NULL, type="l", ylab=NA, xlim = c(xmin,xmax), ylim = c(ymin,ymax), axes=FALSE, 
			frame.plot=FALSE, las=1, tck=.01, mgp=c(3,.5,0), xaxs="i", yaxs="i", font=2)
}

rendergrid<-function(isMulti, isTop){
	if(isMulti&&isTop){
		for(y in seq(altymin, altymax, altyscale))
			lines(x=c(xmin, xmax), y=c(y, y), lty=1, col=gridcolor, lend=endtype, xpd=NA, lwd=lineWidth)
		for(x in seq(xmin, xmax, xscale))
			lines(x=c(x, x), y=c(altymin, altymax),  lty=1, col=gridcolor, lend=endtype, xpd=NA, lwd=lineWidth)
	}else{
		for(y in seq(ymin, ymax, yscale))
			lines(x=c(xmin, xmax), y=c(y, y), lty=1, col=gridcolor, lend=endtype, xpd=NA, lwd=lineWidth)
		for(x in seq(xmin, xmax, xscale))
			lines(x=c(x, x), y=c(ymin, ymax),  lty=1, col=gridcolor, lend=endtype, xpd=NA, lwd=lineWidth)
		if(isMulti){
			for(x in seq(xmin, xmax, xscale))
				lines(x=c(x, x), y=c(ymax, ymax+yinch(mpMedian*ydim)), xpd=NA, col=gridcolor, lwd=lineWidth)
		}
	}
	abline(h=0, lty=1, col=framecolor, lend=endtype, lwd=lineWidth)
	abline(v=0, lty=1, col=framecolor, lend=endtype, lwd=lineWidth)

	if(!is.na(customaxis)){
		rawaxis=list()
		#Loading Axis file
		if(is.null(rawaxis[[customaxis]])){
			cat("   Reading axis file ...\n")
			rawaxis=append(rawaxis, list(read.csv(customaxis, header = TRUE, strip.white=TRUE)))
			names(rawaxis)[length(rawaxis)]=customaxis
		}
		customaxisorder=order(rawaxis[[customaxis]][["yaxis"]])
		cAxis=data.frame(label=rawaxis[[customaxis]][customaxisorder, "label"], yaxis=rawaxis[[customaxis]][customaxisorder, "yaxis"])
		if(is.na(cAxisStart)|is.na(cAxisEnd)){
			par(cex=.5)
			axis(side=4, at=cAxis[[2]], labels=cAxis[[1]], mgp=c(5,.5,0), tck=.01, las=1, yaxs="i", col=framecolor, col.axis=framecolor, lend=endtype, lwd=0, lwd.ticks=lineWidth, cra=c(12,12))
			par(cex=1)
		}
		for(locs in cAxis[[2]]){
			if(!is.na(cAxisStart)&!is.na(cAxisEnd)){
				lines(y=c(locs, locs), x=c(cAxisStart, cAxisEnd), lwd=lineWidth)
				text(x=cAxisEnd, y=locs, labels=cAxis[[1]][match(locs, cAxis[[2]])], pos=4)
			}else
				abline(h=locs, lwd=lineWidth)
		}
	}
}

default=alist(datafile=NULL, vars=NULL, yaxis=NA, timeFile=NA, xaxis="Time (s)", 
		pointsAvg=1, fuzziness=0, yMinDisc=NA, yMaxDisc=NA, legendPos=NA,
		times=1, maxXtick=7, maxYtick=7, xdim=7, ydim=NA, labelMargin=.04, 
		axis2a=NA, suppNames=FALSE, axis2b=0, axis2lab=NA, symbols=10, 
		filename="Unnamed", fileSuffix=NA, norm2zero=NA, timelineOffset=FALSE,
		legendSize=.75, eventMargin=NA, maxDisp=.15, smoothness=10,
		maxOverlap=10, eventLabelBias=.5, plotHeight=NA, endTime=NA, startTime=0,
		singleErrorPercent=0, timeOffset=0, dataCut=NA, folder="",
		singleEvents=TRUE, continuity=0, primary=.95, secondary=.45, bandwidth=.75,
		framecolor="black", endtype="square", legendcols=1, bgcolor="white",
		gridcolor="#f0f0f0", eventcolorhi=.8, eventcolorlow=.4, mpMedian=.05, title=NA,
		outputType="png", lineWidth=2, dataMax=NA, dpi=600, drawLine=FALSE, 
		pointAccent=TRUE, binsize=1, arrowsize=.15, showSamples=FALSE, order=FALSE,
		customaxis=NA, customAxisMargin=2, cAxisStart=NA, cAxisEnd=NA, xvar="time",
		altyMaxDisc=NA, altyMinDisc=NA, reverseVars=FALSE)

if(!is.null(args[["dataFile"]])){ dataFile=args[["dataFile"]] }
else if(!is.null(args[[1]])){ dataFile=args[[1]] }
else{ cat("A non-Null data file is required.") }


if(is.null(args[["vars"]])){
	plots=read.csv(dataFile, header=TRUE, fill=TRUE, blank.lines.skip=TRUE)
	entry=dim(plots)[1]
}else{
	entry=1
	plots=NULL
	vars=list(vars)
}

rawdata=list()
rawtimeline=list()
while(entry>=1){

for(variable in names(default)){ assign(variable,default[[variable]]) }
for(variable in names(args[names(args)%in%names(default)])){ assign(variable,args[names(args)%in%names(default)][[variable]]) }


if(!is.null(plots)){
	curplot=plots[entry, seq(0, (dim(plots)[2]))]
	dataFile=vector()
	dataFileTemp=vector()
	fileSuffix=vector()
	varAverageSet=vector()
	vars=list()
	altVars=list()
	timeOffset=vector()
	dataCut=vector()
	dataCutTemp=vector()


	for(variable in names(curplot)[seq(length(curplot))]){
		if(!is.na(curplot[[variable]])&&!is.null(curplot[[variable]]))
			if(curplot[[variable]]!="")
				if(!is.null(default[[variable]]))
					assign(variable, as.vector(curplot[[variable]]))
				else if(length(grep("^var[[:punct:]]?[[:digit:]]*$", variable))==1){
					if(reverseVars){
						vars=append(as.vector(curplot[[variable]]), vars)
						altVars=append(FALSE, altVars)
						dataFile=append(dataFileTemp, dataFile)
						dataCut=append(dataCutTemp, dataCut)
					}else{
						vars=append(vars, as.vector(curplot[[variable]]))
						altVars=append(altVars, FALSE)
						dataFile=append(dataFile, dataFileTemp)
						dataCut=append(dataCut, dataCutTemp)
					}
				}else if(length(grep("^avg[[:punct:]]?[[:digit:]]*$", variable))==1){
					if(reverseVars)
						varAverageSet=append(as.vector(curplot[[variable]]), varAverageSet)
					else
						varAverageSet=append(varAverageSet, as.vector(curplot[[variable]]))
				}else if(length(grep("^alt[[:punct:]]?[[:digit:]]*$", variable))==1){
					if(reverseVars){
						vars=append(as.vector(curplot[[variable]]), vars)
						altVars=append(TRUE, altVars)
						dataFile=append(dataFileTemp, dataFile)
						dataCut=append(dataCutTemp, dataCut)
					}else{
						vars=append(vars, as.vector(curplot[[variable]]))
						altVars=append(altVars, TRUE)
						dataFile=append(dataFile, dataFileTemp)
						dataCut=append(dataCut, dataCutTemp)
					}
				}else if(length(grep("^data[[:punct:]]?[[:digit:]]*$", variable))==1){
					dataFileTemp=as.vector(curplot[[variable]])	
				}else if(length(grep("^suffix[[:punct:]]?[[:digit:]]*$", variable))==1)
					if(reverseVars)
						fileSuffix=append(as.vector(curplot[[variable]]), fileSuffix)
					else
						fileSuffix=append(fileSuffix, as.vector(curplot[[variable]]))
				else if(length(grep("^line[[:punct:]]?[[:digit:]]*$", variable))==1)
					if(reverseVars)
						drawLine=append(as.vector(curplot[[variable]]), drawLine)
					else
						drawLine=append(drawLine, as.vector(curplot[[variable]]))
				else if(length(grep("^cutoff[[:punct:]]?[[:digit:]]*$", variable))==1)
					dataCutTemp=as.vector(curplot[[variable]])
				else if(length(grep("^offset[[:punct:]]?[[:digit:]]*$", variable))==1)
					if(reverseVars)
						timeOffset=append(as.vector(curplot[[variable]]), timeOffset)
					else
						timeOffset=append(timeOffset, as.vector(curplot[[variable]]))
	}

	if(length(drawLine)==1){
		temp=vector()
		for(i in seq(vars)) temp=append(temp, drawLine)
		drawLine=temp
	}
}

options(warn=-1)
cat("Rendering", filename, "...\n")

#Creating rendering window for reference only
graphics.off()
if(outputType=="wmf")
	win.metafile(paste(paste(folder,filename, sep=""), "wmf", sep="."),xdim,4,12, restoreConsole=FALSE)
if(outputType=="png")
	png(paste(paste(folder,filename, sep=""), "png", sep="."),xdim,1,12, units="in",restoreConsole=FALSE, res=dpi)

if(!is.na(axis2a)&&!is.na(axis2b)&&!is.na(axis2lab))
	par(fig=c(0, 1, 0, 1), bg=bgcolor, mar=c(3,4,1,4)+.01)
else
	par(fig=c(0, 1, 0, 1), bg=bgcolor, mar=c(3,4,1,2)+.01)


for(file in dataFile){
	if(is.null(rawdata[[file]])){
		cat("   Reading data ")
		cat(file)
		cat("...\n")
		rawdata=append(rawdata, list(read.csv(file , header = TRUE, strip.white=TRUE, check.names=FALSE)))
		names(rawdata)[length(rawdata)]=file
	}
}


#loading data files
datafiles=1
data=list()
times=list()
totalvars=0

for(file in dataFile){
	data=append(data, list(rawdata[[file]]))
	vars[datafiles]=list(replace(as.numeric(vars[[datafiles]]), is.na(as.numeric(vars[[datafiles]])),  match(vars[[datafiles]], dimnames(data[[length(data)]])[[2]])))
	vars[datafiles]=list(subset(vars[[datafiles]], !is.na(vars[[datafiles]])))
	times=append(times, list(charmatch(tolower(xvar), tolower(dimnames(data[[length(data)]])[[2]]))))
	if(is.na(times)){
		cat("   Invalid X variable.\n")
		next
	}
	if(length(timeOffset)==1)
		data[[length(data)]][times[[datafiles]]]=data[[length(data)]][times[[datafiles]]]+as.numeric(timeOffset)
	else if(!is.na(timeOffset[datafiles]))
		data[[length(data)]][times[[datafiles]]]=data[[length(data)]][times[[datafiles]]]+as.numeric(timeOffset[datafiles])

	totalvars=totalvars+dim(data.matrix(vars[[datafiles]]))[1]
	datafiles=datafiles+1
}

#Trim data to used variables
datafiles=1
xmax=0
xmin=0
if(!is.na(startTime)){xmin=startTime}
scaledata=FALSE

while(datafiles<=length(data)){
	if(!is.na(norm2zero)){
		if(!is.null(dim(norm2zero))&&dim(norm2zero)[1]==dim(data.matrix(vars[[datafiles]]))[1]){
			norm=norm2zero
		}else{
			if(norm2zero=="B"){
				background=data[[datafiles]][is.na(data[[datafiles]][times[[datafiles]]])|data[[datafiles]][times[[datafiles]]]<=0,seq(dim(data[[datafiles]])[2])]
				background[times[[datafiles]]]=seq(0, by=0, length.out=dim(background)[1])
			}else{
				background=data[[datafiles]][is.na(data[[datafiles]][times[[datafiles]]])|data[[datafiles]][times[[datafiles]]]==0,seq(dim(data[[datafiles]])[2])]
			}
		}
		for(var in seq(2, dim(data[[datafiles]])[2])){
			data[[datafiles]][seq(dim(data[[datafiles]])[1]),var]=data[[datafiles]][seq(dim(data[[datafiles]])[1]),var]-mean(data.matrix(background[var]))
		}
	}
	data[datafiles]=list(as.matrix(cbind(data[[datafiles]][times[[datafiles]]], data[[datafiles]][vars[[datafiles]]])))
	if(dim(data[[datafiles]])[2]<2){
		cat("   Invalid Variable.\n")
		datafiles=datafiles+1
		next
	}

	data[[datafiles]]=data[[datafiles]][!is.na(data[[datafiles]][,2]),seq(2)]
	

	if(!is.na(yMaxDisc)&!altVars[[datafiles]])
		data[[datafiles]]=data[[datafiles]][data[[datafiles]][,2]<yMaxDisc,seq(2)]
	if(length(data[[datafiles]])!=0&!is.na(yMinDisc)&!altVars[[datafiles]])
		data[[datafiles]]=data[[datafiles]][data[[datafiles]][,2]>yMinDisc,seq(2)]
	if(length(data[[datafiles]])!=0&!is.na(altyMaxDisc)&altVars[[datafiles]])
		data[[datafiles]]=data[[datafiles]][data[[datafiles]][,2]<altyMaxDisc,seq(2)]
	if(length(data[[datafiles]])!=0&!is.na(altyMinDisc)&altVars[[datafiles]])
		data[[datafiles]]=data[[datafiles]][data[[datafiles]][,2]>altyMinDisc,seq(2)]


	if(length(data[[datafiles]])==0){
		cat("   Variable \"")
		cat(dimnames(data[[datafiles]])[[2]][2])
		cat("\" contains no usable data.\n")
		datafiles=datafiles+1
		next
	}

	vars[datafiles]=list(seq(2,dim(data.matrix(vars[[datafiles]]))[1]+1))
	data[datafiles]=list(subset(data[[datafiles]], !is.na(data[[datafiles]][seq(dim(data[[datafiles]])[1])])&data[[datafiles]][seq(dim(data[[datafiles]])[1])]>=startTime))	
	if(any(altVars[[datafiles]])){
		scaledata=TRUE
	}
	if(!is.na(dataCut[datafiles])){
		data[datafiles]=list(subset(data[[datafiles]], data[[datafiles]][seq(dim(data[[datafiles]])[1])]<=dataCut[datafiles]))	
	}
	if(length(dataCut)==1){
		data[datafiles]=list(subset(data[[datafiles]], data[[datafiles]][seq(dim(data[[datafiles]])[1])]<=dataCut))	
	}
	if(!is.na(endTime))
		xmax=endTime
	else
		xmax=max(c(xmax, data.matrix(data[[datafiles]][seq(dim(data[[datafiles]])[1])])), rm.na=TRUE)
	datafiles=datafiles+1
}


if(xmax==xmin){
	cat("   Variable contains trivial data.\n")
	dev.off(which = dev.cur())
	entry=entry-1
	next
}
axisvars=axisscale(xmax, xmin, xmult, xscale, maxXtick)
xmax=axisvars[1]
xmin=axisvars[2]
xmult=axisvars[3]
xscale=axisvars[4]
xmin=floor(xmin/xscale)*xscale
xmax=ceiling(xmax/xscale)*xscale
xticks=(xmax-xmin)/xscale
if(length(varAverageSet)>0){
	j = 1
	k = 1
	datatemp=list()
	avgnumber=list()
	for(var2avg in data){
		var2avg[,1]=round(var2avg[,1]/binsize)*binsize
		i = 1
		while(i < nrow(var2avg)){
			if(length(datatemp)==0){
				datatemp=list(var2avg[i,])
				avgnumber=list(1)
			}else{
				if(k <= varAverageSet[j]){
					matches=match(var2avg[i,1],as.matrix(datatemp[[j]])[,1])
					if(is.na(matches)){
						datatemp[[j]]=rbind(datatemp[[j]],var2avg[i,])
						avgnumber[[j]]=rbind(avgnumber[[j]],1)
					}else{
						if(is.null(nrow(datatemp[[j]])))
							datatemp[[j]][2]=(datatemp[[j]][2]*avgnumber[[j]][matches]+var2avg[i,2])/(avgnumber[[j]][matches]+1)
						else
							datatemp[[j]][matches,2]=(datatemp[[j]][matches,2]*avgnumber[[j]][matches]+var2avg[i,2])/(avgnumber[[j]][matches]+1)
						avgnumber[[j]][matches]=avgnumber[[j]][matches]+1
					}
				}else{
					datatemp=append(datatemp,list(var2avg[i,]))
					avgnumber=append(avgnumber, list(1))
					k=1
					j=j+1
				}
			}
			i=i+1
		}
		k=k+1
	}
	if(showSamples)
		data=append(data,datatemp)
	else
		data=datatemp
	totalvars=length(data)
	vars=as.list(seq(data)*0+2)
	altVars=as.list(as.logical(seq(data)*0))
	
}


datafiles=1
ymin=0
ymax=0
altymin=0
altymax=0

while(datafiles<=length(data)){
	if(length(data[[datafiles]])==0){
		datafiles=datafiles+1
		next
	}
	#Average Times and Data into bins, each bin is of size pointsAvg seconds
	if(pointsAvg>1){
		cat("   Averaging...\n")
		reduxdata=vector()
		for(n in seq(floor(min(data[[datafiles]][seq(dim(data[[datafiles]])[1])])/pointsAvg), ceiling(max(data[[datafiles]][seq(dim(data[[datafiles]])[1])])/pointsAvg))){
			reduxdata=rbind(reduxdata,mean(data.frame(subset(data[[datafiles]], (data[[datafiles]][seq(dim(data[[datafiles]])[1])]<=pointsAvg*n)&(data[[datafiles]][seq(dim(data[[datafiles]])[1])]>pointsAvg*(n-1))), check.names=FALSE), rm.na=TRUE))
		}
		reduxdata=subset(reduxdata,!is.nan(reduxdata[seq(dim(reduxdata)[1])]))
		data[datafiles]=list(reduxdata)
	}
	if(fuzziness>0){
			cat("   Smoothing...\n")
			newtimes=seq(from=min(data[[datafiles]][, 1]), to=max(data[[datafiles]][, 1]), length.out=smoothness*dim(data[[datafiles]])[1]-smoothness+1)
			oldtimes=data[[datafiles]][, 1]
			reduxdata=vector()
			if(continuity>0){
				oldpoint=data[[datafiles]][1, seq(2, dim(data[[datafiles]])[2])]
				for(timeindex in seq(length(newtimes))){
					weight=exp(-log((fuzziness+1)/fuzziness)*(oldtimes-newtimes[timeindex])*log((continuity+1)/continuity)*(data[[datafiles]][seq(dim(data[[datafiles]])[1]), seq(2, dim(data[[datafiles]])[2])]-oldpoint))
					oldpoint=colSums(weight*data[[datafiles]][seq(dim(data[[datafiles]])[1]), seq(2, dim(data[[datafiles]])[2])])/colSums(weight)
					reduxdata=rbind(reduxdata, oldpoint)
				}
			}else{
				for(time in newtimes){
					weight=(1+1/fuzziness)^(-abs(oldtimes-time))
					reduxdata=rbind(reduxdata, colSums(weight*data[[datafiles]][seq(dim(data[[datafiles]])[1]), seq(2, dim(data[[datafiles]])[2])])/sum(weight))
				}
			}
			reduxdata=cbind(Time=newtimes, reduxdata)
			data[datafiles]=list(reduxdata)
	}
	
	dataset=as.matrix(data[[datafiles]][, vars[[datafiles]]])
	if(singleErrorPercent==0)
		barRange=dataset
	else
		barRange=subset(dataset, data[[datafiles]][seq(dim(data.matrix(dataset))[1])]<(xmax-(xmax-xmin)*.05)&data[[datafiles]][seq(dim(data.matrix(dataset))[1])]>(xmin+(xmax-xmin)*.05))*(1+singleErrorPercent)
	datasetDim=seq(dim(dataset)[1])
	##Replacing empty data cells with ymin
	ymin=min(c(ymin, dataset[ datasetDim, !altVars[[datafiles]] ], barRange[ seq(dim(barRange)[1]), !altVars[[datafiles]] ]))
	ymax=max(c(ymax, dataset[ datasetDim, !altVars[[datafiles]] ], barRange[ seq(dim(barRange)[1]), !altVars[[datafiles]] ]))
	altymin=min(c(altymin, dataset[ datasetDim, altVars[[datafiles]] ], barRange[ seq(dim(barRange)[1]), altVars[[datafiles]] ]))
	altymax=max(c(altymax, dataset[ datasetDim, altVars[[datafiles]] ], barRange[ seq(dim(barRange)[1]), altVars[[datafiles]] ]))
	datafiles=datafiles+1
}

if(scaledata)
	maxYtick=maxYtick/2

if(!is.na(dataMax))
	ymax=dataMax

if(ymax==ymin){
	cat("   Variable contains trivial data.\n")
	dev.off(which = dev.cur())
	entry=entry-1
	next
}
axisvars=axisscale(ymax, ymin, ymult, yscale, maxYtick)
ymax=axisvars[1]
ymin=axisvars[2]
ymult=axisvars[3]
yscale=axisvars[4]

if(scaledata){
	if(altymax==altymin){
		cat("   Variable contains trivial data.\n")
		dev.off(which = dev.cur())
		entry=entry-1
		next
	}
	axisvars=axisscale(altymax, altymin, altymult, altyscale, maxYtick)
	altymax=axisvars[1]
	altymin=axisvars[2]
	altymult=axisvars[3]
	altyscale=axisvars[4]
	altymin=floor(altymin/altyscale)*altyscale
	altymax=ceiling(altymax/altyscale)*altyscale
	altyticks=(altymax-altymin)/altyscale
}

ymin=floor(ymin/yscale)*yscale
ymax=ceiling(ymax/yscale)*yscale
yticks=(ymax-ymin)/yscale

if(is.na(eventMargin)&&!is.na(plotHeight)&&!is.na(ydim)){ eventMargin=ydim-plotHeight-ydim*labelMargin }
if(is.na(eventMargin)){ eventMargin=0 }

if(!is.na(timeFile)){

#Rendering the scatter plot
plot.default(NULL, type="l", ylab=NA, xlim = c(xmin,xmax), ylim = c(ymin,ymax), axes=FALSE, 
	frame.plot=FALSE, las=1, tck=.01, mgp=c(3,.5,0), xaxs="i", yaxs="i", font=2)

#Loading Timeline file
if(is.null(rawtimeline[[timeFile]])){
	cat("   Reading timeline file ...\n")
	rawtimeline=append(rawtimeline, list(read.csv(timeFile, header = TRUE, strip.white=TRUE)))
	names(rawtimeline)[length(rawtimeline)]=timeFile
}
eventorder=order(rawtimeline[[timeFile]][["start"]])

if(any(names(rawtimeline[[timeFile]])=="end")){
	if(length(timeOffset)==0|!timelineOffset){
		timeline=data.frame(event=rawtimeline[[timeFile]][eventorder, "event"], start=rawtimeline[[timeFile]][eventorder, "start"], end=rawtimeline[[timeFile]][eventorder, "end"])
	}else{
		timeline=data.frame(event=rawtimeline[[timeFile]][eventorder, "event"], start=rawtimeline[[timeFile]][eventorder, "start"]+timeOffset, end=rawtimeline[[timeFile]][eventorder, "end"]+timeOffset)
	}
}else{
	if(length(timeOffset)==0|!timelineOffset){
		timeline=data.frame(event=rawtimeline[[timeFile]][eventorder, "event"], start=rawtimeline[[timeFile]][eventorder, "start"])
	}else{
		timeline=data.frame(event=rawtimeline[[timeFile]][eventorder, "event"], start=rawtimeline[[timeFile]][eventorder, "start"]+timeOffset)
	}
}
timeline=subset(timeline, timeline["start"]<=xmax&timeline["start"]>=xmin)

charHeight=strheight("/_GypL", units="inches")+.05
charWidth=max(strwidth(timeline[["event"]], units="inches"))+.05

overlap=NULL

	cat("   Calculating label positions ...\n")
	oldMargin=NULL
	oldLocs=NULL
	oldScore=NULL
	oldOverlap=NULL
	notPass=TRUE
	while(notPass){
		notPass=FALSE
		eventLocs=eventLocation(xmin, xmax, 0, NA)
		if(is.null(eventLocs)){
			notPass=TRUE
			eventMargin=eventMargin+.1
		}else{
			#Creating a list of vertical displacements for line structure on timeline data
			#they should be maximally spaced in the label margin
			overlap=seq(dim(timeline["start"])[1])*0
			
			#First (right) pass of the line offsetting process,
			#evaluates whether (left)labels to (right) lines should be displaced further up
			n=2
			while(n<=length(eventLocs[["location"]])){
				if(eventLocs[["location"]][n]<=data.matrix(timeline["start"])[n-1]){
					overlap[n]=overlap[n-1]+1
				}
				n=n+1
			}
			#Second (left) pass of the line offsetting process
			#evaluates whether (right) labels to (left) lines should be displaced further up
			n=length(eventLocs[["location"]])-1
			while(n>=1){
				if(eventLocs[["location"]][n]>=data.matrix(timeline["start"])[n+1]){
					overlap[n]=overlap[n+1]+1
				}
				n=n-1
			}
			if(max(sqrt(((timeline[["start"]]-eventLocs[["location"]])/(xmax-xmin)/maxDisp)^2+(overlap/maxOverlap)^2))>1){
				oldMargin=c(eventMargin, oldMargin)
				oldScore=c(max(sqrt(((timeline[["start"]]-eventLocs[["location"]])/(xmax-xmin)/maxDisp)^2+(overlap/maxOverlap)^2)), oldScore)
				oldLocs=c(list(eventLocs), oldLocs)
				oldOverlap=c(list(overlap), oldOverlap)
				notPass=TRUE
				eventMargin=eventMargin+.1
				if(eventLocs[["theta"]]==pi/2||(!is.na(ydim)&&!is.na(plotHeight)&&eventMargin>=ydim-plotHeight)){
					eventLocs=oldLocs[[which.min(oldScore)]]
					eventMargin=oldMargin[which.min(oldScore)]
					overlap=oldOverlap[[which.min(oldScore)]]
					notPass=FALSE
				}
			}
		}
	}
}

ydim=createwindow(ydim)

renderplotspace(scaledata, FALSE)
rendergrid(scaledata, FALSE)
if(!is.na(timeFile))
	renderablines(scaledata, FALSE)
errorBarX=NULL
errorBarY=NULL
errorBar=rendererrorbar(scaledata, FALSE)
renderpoints(scaledata, FALSE, FALSE)
if(totalvars>1)
	renderpoints(scaledata, FALSE, TRUE)
renderaxes(scaledata, FALSE)
renderlegend(scaledata, FALSE, errorBar[[1]], errorBar[[2]])

if(scaledata){
	renderplotspace(scaledata, TRUE)
	rendergrid(scaledata, TRUE)
	if(!is.na(timeFile))
		renderablines(scaledata, TRUE)
	errorBar=rendererrorbar(scaledata, TRUE)
	renderpoints(scaledata, TRUE, FALSE)
	renderpoints(scaledata, TRUE, TRUE)
	renderaxes(scaledata, TRUE)
	renderlegend(scaledata, TRUE, errorBar[[1]], errorBar[[2]])
}


if(!is.na(timeFile))
	rendertimeline(scaledata)

renderplotspace(FALSE, TRUE)
mtext(yaxis, side=2, line=3, font=2, col=framecolor)


dev.off(which = dev.cur())
entry=entry-1
}
}

#plotdata("PA Plots 2.csv", maxXtick=10, folder="Plot Output/", lineWidth=2, outputType="png", drawLine=FALSE, maxDisp=.3, framecolor="black")
#plotdata("Mystery Plot Setup.csv", maxXtick=10, folder="Plot Output/", lineWidth=2, framecolor="black", outputType="png", drawLine=FALSE, eventcolorhi=.30, eventcolorlow=.30)
#plotdata("BasementInput.csv", folder="646B_Plots/")
#plotdata("BP plots Avg.csv", folder="Plot Output/")
#plotdata("FOS RAW.csv", folder="", drawLine=TRUE)
plotdata("225_test1_input.csv", maxXtick=10, outputType="png", symbols=10, lineWidth=2, drawLine=TRUE)
#plotdata("644A_HFinput.csv", maxXtick=10, outputType="png", symbols=10, lineWidth=2, drawLine=TRUE)
#plotdata("Lawson RFID.csv", arrowsize=NA, outputType="pn")
#plotdata("parkway ter/PT Plot.csv", arrowsize=NA, reverseVars=FALSE)