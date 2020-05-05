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
module fsm_frac_sec (clk ,ce ,hard_rst, gpio,new_count, waiting, threshold, state );


output new_count;
wire new_count;
output[2:0] state;
wire [2:0]	state;

input clk;
wire clk;
input ce;
wire ce;
input hard_rst;
wire hard_rst;
input gpio;
wire gpio;
input [31:0] threshold;
wire [31:0] threshold;
input [31:0] waiting;
wire [31:0]  waiting;  

reg[31:0] aux;
reg[31:0] aux_wait;
reg[31:0] counter=0;
reg[2:0] actual_state;
reg[2:0] next_state;

reg new_count_r = 0;

parameter start = 3'b000;
parameter a = 3'b100;
parameter b = 3'b101;
parameter c = 3'b001;
parameter d = 3'b011;
parameter e = 3'b111;
parameter f = 3'b110;


// -- Enter your statements here -- //

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
			if(gpio)        next_state = b;
			else            next_state = a;
		b:
         		begin
				if(counter >aux)                 next_state = c;
				else if (~gpio)			 next_state = start;
				else                         	 next_state = b;
         		end		
      		c:
			next_state = d;
		d:
			if(counter>aux_wait)			next_state = e;
			else					next_state = d;
		e:
			if(~gpio)				next_state = f;
			else					next_state = e;
		f: 
			next_state = a;
	endcase
end


always@(posedge clk) begin
	case(actual_state) 
		start: 
		begin
				aux = threshold;
				new_count_r = 0;
				aux_wait = waiting;	
		end
		b:
			counter = counter+1;
		c:
			begin
				new_count_r = 1;
				counter = 0;
			end
     		d: 
			begin
				counter = counter+1;
				new_count_r = 0;
			end
		f:
			counter = 0;
	endcase
end
assign new_count = new_count_r;
assign state = actual_state;
endmodule
