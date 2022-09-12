import { Component, OnInit } from '@angular/core';
import { Outcome } from 'src/app/models/outcome';

@Component({
  selector: 'app-scheme',
  templateUrl: './scheme.component.html',
  styleUrls: ['./scheme.component.scss']
})
export class SchemeComponent implements OnInit {

  constructor() { }

  ngOnInit(): void {
    var self = this;

    var canvas: any = document.getElementById("np-canvas");

    var translatePos = {
        x: canvas.width / 2,
        y: canvas.height / 2
    };

    var scale = 1.0;
    var scaleMultiplier = 0.8;
    var startDragOffset: any = {};
    var mouseDown = false;

    // add button event listeners
    document.getElementById("plus").addEventListener("click", function(){
        scale /= scaleMultiplier;
        self.draw(scale, translatePos);
    }, false);

    document.getElementById("minus").addEventListener("click", function(){
        scale *= scaleMultiplier;
        self.draw(scale, translatePos);
    }, false);

    // add event listeners to handle screen drag
    canvas.addEventListener("mousedown", function(evt){
        mouseDown = true;
        startDragOffset.x = evt.clientX - translatePos.x;
        startDragOffset.y = evt.clientY - translatePos.y;
    });

    canvas.addEventListener("mouseup", function(evt){
        mouseDown = false;
    });

    canvas.addEventListener("mouseover", function(evt){
        mouseDown = false;
    });

    canvas.addEventListener("mouseout", function(evt){
        mouseDown = false;
    });

    canvas.addEventListener("mousemove", function(evt){
        if (mouseDown) {
            translatePos.x = evt.clientX - startDragOffset.x;
            translatePos.y = evt.clientY - startDragOffset.y;
            self.draw(scale, translatePos);
        }
    });

    self.draw(scale, translatePos);
  }

  draw(scale, translatePos) {
    // canvas sizes
    var cwidth = 851;
    var cheight = 500;

    var ltpx = -(cwidth/2.0);
    var ltpy = -(cheight/2.0);

    // colors
    
    // Целевая группа 
    var targetFill = "#9ee8f4"; 
    var targetBorder = "#45c6db";
    
    // Активность
    var activityFill = "#adfbdd"; 
    var activityBorder = "#2ca978";
    
    // Непосредственный результат
    var outputFill = "#fee6b1"; 
    var outputBorder = "#ee860b";
    
    // Краткосрочный социальный результат
    var shortOutcomeFill = "#f3c9ee"; 
    var shortOutcomeBorder = "#bf44af";
    
    // Среднесрочный социальный результат
    var midOutcomeFill = "#c1b9f4"; 
    var midOutcomeBorder = "#6a5faf";
    
    // Социальный эффект
    var impactFill = "#f4c2b9"; 
    var impactBorder = "#ff330b";

    var canvas:any = document.getElementById("np-canvas");
    var context = canvas.getContext("2d");

    // clear canvas
    // work with zooming, do not touch
    context.clearRect(0, 0, canvas.width, canvas.height);

    context.save();
    context.translate(translatePos.x, translatePos.y);
    context.scale(scale, scale);
    //  end of work with zooming, do not touch

    // border of initiating canvas. for debug only
    context.strokeStyle = "#000000";
    context.strokeRect(ltpx-1, ltpy-1, cwidth+2, cheight+2);

    var i = 0;
    context.strokeStyle = impactBorder;
    context.strokeRect(ltpx, ltpy + (cheight/6.0)*i, cwidth, cheight/6.0);
    context.strokeRect(ltpx + (cheight/18.0), ltpy + (cheight/6.0)*i + (cheight/18.0), cwidth - (cheight/9.0), cheight/18.0);
    var impactY = ltpy + (cheight/6.0)*i + (cheight/18.0);

    i += 1;
    context.strokeStyle = midOutcomeBorder;
    context.strokeRect(ltpx, ltpy + (cheight/6.0)*i, cwidth, cheight/6.0);
    context.strokeRect(ltpx + (cheight/18.0), ltpy + (cheight/6.0)*i + (cheight/18.0), cwidth - (cheight/9.0), cheight/18.0);
    var midOutcomeY = ltpy + (cheight/6.0)*i + (cheight/18.0);

    i += 1;
    context.strokeStyle = shortOutcomeBorder;
    context.strokeRect(ltpx, ltpy + (cheight/6.0)*i, cwidth, cheight/6.0);
    context.strokeRect(ltpx + (cheight/18.0), ltpy + (cheight/6.0)*i + (cheight/18.0), cwidth - (cheight/9.0), cheight/18.0);
    var shortOutcomeY = ltpy + (cheight/6.0)*i + (cheight/18.0);

    i += 1;
    context.strokeStyle = outputBorder;
    context.strokeRect(ltpx, ltpy + (cheight/6.0)*i, cwidth, cheight/6.0);
    context.strokeRect(ltpx + (cheight/18.0), ltpy + (cheight/6.0)*i + (cheight/18.0), cwidth - (cheight/9.0), cheight/18.0);
    var outputY = ltpy + (cheight/6.0)*i + (cheight/18.0);

    i += 1;
    context.strokeStyle = activityBorder;
    context.strokeRect(ltpx, ltpy + (cheight/6.0)*i, cwidth, cheight/6.0);
    context.strokeRect(ltpx + (cheight/18.0), ltpy + (cheight/6.0)*i + (cheight/18.0), cwidth - (cheight/9.0), cheight/18.0);
    var activityY = ltpy + (cheight/6.0)*i + (cheight/18.0);

    i += 1;
    context.strokeStyle = targetBorder;
    context.strokeRect(ltpx, ltpy + (cheight/6.0)*i, cwidth, cheight/6.0);
    context.strokeRect(ltpx + (cheight/18.0), ltpy + (cheight/6.0)*i + (cheight/18.0), cwidth - (cheight/9.0), cheight/18.0);
    var targetY = ltpy + (cheight/6.0)*i + (cheight/18.0);
    // end of border of initiating canvas. for debug only

    // data

    // var outcomes:Outcome[] = [
    //   new Outcome() {name: 'Улучшение эмоционального состояния ребенка'},
    //   {name: 'Повышен уровень социально-бытовой адаптации'},
    //   {name: 'Улучшение внутрисемейных отношений, включая детско-родительские отношения'},
    // ];
    
    // end of data
    
        context.strokeStyle = impactBorder;
        context.fillStyle = impactFill;


    // context.strokeStyle = "#0000ff";
    // context.fillStyle = "#aaaaee";

    // this.roundRect(context, -10, -10, 20, 20, 1, true, true);

    // context.fill();

    // context.lineWidth = 5;
    // context.strokeStyle = "#0000ff";
    // context.stroke();
    context.restore();
  }

  roundRect(ctx, x, y, width, height, radius, fill, stroke) {
    if (typeof stroke === 'undefined') {
      stroke = true;
    }
    if (typeof radius === 'undefined') {
      radius = 5;
    }
    if (typeof radius === 'number') {
      radius = {tl: radius, tr: radius, br: radius, bl: radius};
    } else {
      var defaultRadius = {tl: 0, tr: 0, br: 0, bl: 0};
      for (var side in defaultRadius) {
        radius[side] = radius[side] || defaultRadius[side];
      }
    }
    ctx.beginPath();
    ctx.moveTo(x + radius.tl, y);
    ctx.lineTo(x + width - radius.tr, y);
    ctx.quadraticCurveTo(x + width, y, x + width, y + radius.tr);
    ctx.lineTo(x + width, y + height - radius.br);
    ctx.quadraticCurveTo(x + width, y + height, x + width - radius.br, y + height);
    ctx.lineTo(x + radius.bl, y + height);
    ctx.quadraticCurveTo(x, y + height, x, y + height - radius.bl);
    ctx.lineTo(x, y + radius.tl);
    ctx.quadraticCurveTo(x, y, x + radius.tl, y);
    ctx.closePath();
    if (fill) {
      ctx.fill();
    }
    if (stroke) {
      ctx.stroke();
    }
  
  }

}
