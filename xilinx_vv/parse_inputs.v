//-----------------------------------------------------------------------------
//
// Title       : parse_inputs
// Design      : irig_read_input
// Author      : Seba
// Company     : Universidad de Chile
//
//-----------------------------------------------------------------------------
//
// File        : c:\Users\seba\Documents\active-hdl\irig_read_input\irig_read_input\src\parse_inputs.v
// Generated   : Thu Feb  7 01:13:07 2019
// From        : interface description file
// By          : Itf2Vhdl ver. 1.22
//
//-----------------------------------------------------------------------------
//
// Description : 
//
//-----------------------------------------------------------------------------
`timescale 1 ns / 1 ps

//{{ Section below this comment is automatically maintained
//   and may be overwritten
//{module {parse_inputs}}
module parse_inputs ( clk ,ce ,hard_rst ,rst ,gpio ,cal ,in_frame ,terminate ,cont ,en_ind ,rst_ind ,data_ready ,en_cbh ,rst_cbh, state_out, reg_wait);

output en_ind ;
wire en_ind ;
output rst_ind ;
wire rst_ind ;
output data_ready ;
wire data_ready ;
output en_cbh ;
wire en_cbh ;
output rst_cbh ;
wire rst_cbh ;
output [3:0] state_out;
wire  [3:0] state_out;

input clk ;
wire clk ;
input ce ;
wire ce ;
input hard_rst ;
wire hard_rst ;
input rst ;
wire rst ;
input gpio ;
wire gpio ;
input cal ;
wire cal ;
input in_frame ;
wire in_frame ;
input terminate ;
wire terminate ;
input cont ;
wire cont ;
input[31:0] reg_wait;
wire[31:0] reg_wait;
//}} End of automatically maintained section

// -- Enter your statements here -- //
reg[31:0] aux;
reg[31:0] counter = 0;
reg[3:0] next_state;
parameter start = 4'b1011;
parameter a = 4'b1010;
parameter b = 4'b0010;
parameter c = 4'b0000;
parameter d = 4'b1101;
parameter e = 4'b1111;
parameter f = 4'b1110;
parameter g = 4'b1000;
parameter h = 4'b0101;
parameter i = 4'b1100;
parameter j = 4'b0001;
parameter k = 4'b1001;
parameter l = 4'b0100;
parameter m = 4'b0110;
reg[3:0] actual_state = start;
reg en_ind_r=0, rst_ind_r=0, en_cbh_r=0, rst_cbh_r=0, data_ready_r=0;

always@(posedge clk, posedge hard_rst)begin
	if(hard_rst)
		actual_state <= start;
	else
		actual_state <= next_state;
end
	
always@(*)begin
	case(actual_state)
		start:
			next_state = a; 
		a:
			next_state = b;
		b:
			if(~cal)		next_state = b;
			else if(cal)	next_state = c;
		c:
			next_state = h;
		d:
			if(~gpio)		next_state = d;
			else if(gpio)	next_state = e;
		e:
			if(gpio)		next_state = e;
			else if(~gpio)	next_state = m;
		f:	
			next_state = g;
		g:
			if(terminate)	next_state = a;
			else if(rst& ~terminate)	next_state = k;
			else if(in_frame & ~rst & ~terminate )	next_state = i;
			else if(cont & ~in_frame & ~rst & ~terminate)	next_state = c;
			else	next_state = g;
		h:
			next_state = d;
		i:
			next_state = j;
		j:
			next_state = c;
		k:
			next_state = l;
		l:
			next_state = c;
      m:
			begin
				if(aux < counter)	next_state = f;
				else              next_state = c;
			end
	endcase
end

always@(posedge clk) begin
	case(actual_state) 
		start: 
		begin
			data_ready_r = 0;
			en_ind_r = 0;
			rst_ind_r = 1;
			en_cbh_r = 0;
			rst_cbh_r = 1;
         aux = reg_wait;
		end
		a:
			rst_ind_r = 1;
		b:
			rst_ind_r = 0;
		c:
			begin
				rst_cbh_r = 1;
				counter = 0;
			end
		e:
			begin
			en_cbh_r = 1;
         counter = counter +1;
			end
		f:
		begin
			en_cbh_r = 0;
			data_ready_r = 1;
		end
		g:
			data_ready_r = 0;
		h: 
			rst_cbh_r = 0;
		i:
			en_ind_r = 1;
		j:
			en_ind_r = 0;
		k: 
			begin
			en_ind_r = 0;
			rst_ind_r = 1;
			end
		l:
			rst_ind_r = 0;
      m:
			en_cbh_r = 0;
	endcase
end

assign data_ready = data_ready_r;
assign en_ind = en_ind_r;
assign rst_ind = rst_ind_r;
assign en_cbh = en_cbh_r;
assign rst_cbh = rst_cbh_r;
assign state_out = actual_state;
endmodule
