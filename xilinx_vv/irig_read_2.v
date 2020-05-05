//-----------------------------------------------------------------------------
//
// Title       : irig_read_2
// Design      : irig_read
// Author      : Seba
// Company     : Universidad de Chile
//
//-----------------------------------------------------------------------------
//
// File        : c:\Users\seba\Documents\active-hdl\irig_read\irig_read\src\irig_read_2.v
// Generated   : Mon Feb 18 19:36:10 2019
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
//{module {irig_read_2}}
module irig_read_2 ( clk ,ce ,state ,en ,irig_data ,cal ,hrd_rst ,ind ,write ,dir ,start ,rst_reg ,cont ,in_frame ,terminate ,issue, aux_out );

output [3:0] aux_out;
wire [3:0] aux_out;
output [4:0] state ;
wire [4:0] state ;
output write ;
wire write ;
output [3:0] dir ;
wire [3:0] dir ;
output start ;
wire start ;
output rst_reg ;
wire rst_reg ;
output cont ;
wire cont ;
output in_frame ;
wire in_frame ;
output terminate ;
wire terminate ;
output issue ;
wire issue ;

input clk ;
wire clk ;
input ce ;
wire ce ;
input en ;
wire en ;
input [2:0] irig_data ;
wire [2:0] irig_data ;
input cal ;
wire cal ;
input hrd_rst ;
wire hrd_rst ;
input [7:0] ind ;
wire [7:0] ind ;


reg[1:0] count;
reg[7:0] count_fin;
reg[3:0] aux;

reg[4:0] next_state;



parameter start_state = 5'b01111;
parameter a = 5'b01110;
parameter b = 5'b01100;
parameter c = 5'b01101;
parameter d = 5'b11101;
parameter e = 5'b11001;
parameter f = 5'b01001;
parameter g = 5'b10111;
parameter h = 5'b10101;
parameter i = 5'b10011;
parameter j = 5'b10010;
parameter k = 5'b00110;
parameter l = 5'b00010;
parameter m = 5'b10100;
parameter n = 5'b10110;
parameter o = 5'b11110;
parameter p = 5'b10000;
parameter q = 5'b00000;
parameter r = 5'b00100;
parameter s = 5'b00101;
parameter t = 5'b10001;
parameter u = 5'b00001;
parameter v = 5'b01000;
parameter x = 5'b11100;	  
parameter y = 5'b01011;
parameter z = 5'b11111;
parameter aa = 5'b11000;
parameter [7:0]val = 8'b00000011;
reg[3:0]dir_dic[0:100]; 

/* =  ' {4'b1111, 4'b0000, 4'b0000, 4'b0000, 4'b0000, 4'b1111, 4'b0001, 4'b0001, 4'b0001, 4'b1100, 
                                4'b0010, 4'b0010, 4'b0010, 4'b0010, 4'b1111, 4'b0011, 4'b0011, 4'b0011, 4'b1111, 4'b1100,
                                4'b0100, 4'b0100, 4'b0100, 4'b0100, 4'b0111, 4'b0101, 4'b0101, 4'b1111, 4'b1111, 4'b1100,
                                4'b0110, 4'b0110, 4'b0110, 4'b0110, 4'b1111, 4'b0111, 4'b0111, 4'b0111, 4'b0111, 4'b1100,
                                4'b1000, 4'b1000, 4'b1111, 4'b1111, 4'b1111, 4'b1111, 4'b1111, 4'b1111, 4'b1111, 4'b1111};  //es el directorio con las direcciones , hay que definirlo aun...

*/

reg terminate_, cont_, in_frame_, issue_, rst_reg_, start_, write_;
reg[3:0] dir_;

reg[4:0] actual_state=start_state;


initial begin
    dir_dic[0] = 4'b1111; dir_dic[1] = 4'b0000; dir_dic[2]=4'b0000; dir_dic[3]=4'b0000; dir_dic[4]=4'b0000; dir_dic[5]=4'b1111; dir_dic[6]=4'b0001; dir_dic[7]=4'b0001; dir_dic[8] = 4'b0001; dir_dic[9] = 4'b1100;
    dir_dic[10] = 4'b0010; dir_dic[11] = 4'b0010; dir_dic[12] = 4'b0010; dir_dic[13] = 4'b0010; dir_dic[14]=4'b1111;dir_dic[15] = 4'b0011; dir_dic[16] = 4'b0011; dir_dic[17] = 4'b0011; dir_dic[18] = 4'b1111; dir_dic[19] = 4'b1100;
    dir_dic[20] = 4'b0100; dir_dic[21] = 4'b0100; dir_dic[22] = 4'b0100; dir_dic[23] = 4'b0100; dir_dic[24] = 4'b1111; dir_dic[25] = 4'b0101; dir_dic[26] = 4'b0101; dir_dic[27] = 4'b1111; dir_dic[28] = 4'b1111; dir_dic[29] = 4'b1100;
    dir_dic[30] = 4'b0110; dir_dic[31] = 4'b0110; dir_dic[32] = 4'b0110; dir_dic[33]=4'b0110; dir_dic[34] = 4'b1111; dir_dic[35] = 4'b0111; dir_dic[36] = 4'b0111; dir_dic[37] = 4'b0111; dir_dic[38] = 4'b0111; dir_dic[39] = 4'b1100;
    dir_dic[40] = 4'b1000; dir_dic[41] = 4'b1000; dir_dic[42] = 4'b1111; dir_dic[43]=4'b1111; dir_dic[44] = 4'b1111; dir_dic[45] = 4'b1111; dir_dic[46] = 4'b1111; dir_dic[47] = 4'b1111; dir_dic[48] = 4'b1111; dir_dic[49] = 4'b1100;
dir_dic[50] = 4'b1111; dir_dic[51] = 4'b1111; dir_dic[52] = 4'b1111; dir_dic[52] = 4'b1111; dir_dic[53] = 4'b1111; dir_dic[54] = 4'b1111; dir_dic[55] = 4'b1111; dir_dic[56] = 4'b1111; dir_dic[57] = 4'b1111; dir_dic[58] = 4'b1111; dir_dic[59] = 4'b1111;
dir_dic[60] = 4'b1111; dir_dic[61] = 4'b1111; dir_dic[62] = 4'b1111; dir_dic[63] = 4'b1111; dir_dic[64] = 4'b1111; dir_dic[65] = 4'b1111; dir_dic[66] = 4'b1111; dir_dic[67] = 4'b1111; dir_dic[68] = 4'b1111; dir_dic[69] = 4'b1111;
dir_dic[70] = 4'b1111; dir_dic[71] = 4'b1111; dir_dic[72] = 4'b1111; dir_dic[73] = 4'b1111; dir_dic[74] = 4'b1111; dir_dic[75] = 4'b1111; dir_dic[76] = 4'b1111; dir_dic[77] = 4'b1111; dir_dic[78] = 4'b1111; dir_dic[79] = 4'b1111;
dir_dic[80] = 4'b1111; dir_dic[81] = 4'b1111; dir_dic[82] = 4'b1111; dir_dic[83] = 4'b1111; dir_dic[84] = 4'b1111; dir_dic[85] = 4'b1111; dir_dic[86] = 4'b1111; dir_dic[87] = 4'b1111; dir_dic[88] = 4'b1111; dir_dic[89] = 4'b1111;
dir_dic[90] = 4'b1111; dir_dic[91] = 4'b1111; dir_dic[92] = 4'b1111; dir_dic[93] = 4'b1111; dir_dic[94] = 4'b1111; dir_dic[95] = 4'b1111; dir_dic[96] = 4'b1111; dir_dic[97] = 4'b1111; dir_dic[98] = 4'b1111; dir_dic[99] = 4'b1111;
dir_dic[100] = 4'b1111;

rst_reg_ = 0;
cont_ = 0;
dir_ = 4'b1111;
start_ = 0;
write_ = 0;
in_frame_ = 0;
terminate_ =0;
issue_ = 0;
aux = 4'b1111;
end

always@(posedge clk, posedge hrd_rst)begin
	if(hrd_rst)
		actual_state <= start_state;
	else
		actual_state <= next_state;
end

always@(*)begin
	case(actual_state)
	   	start_state:
	   		next_state = a;
	   	a:
	   		next_state = b;
	   	b:	
	   		if(~cal)		next_state = b;
		   	else if(cal)	next_state = c;
	   	c:
	   		next_state = d;
	   	d:
	   		next_state = e;
	   	e:
	   		if(~en)			next_state = e;
	   		else if(en)		next_state = f;
	   	f:
	   		next_state = y;
	   	g:
			next_state = h;		
		h:
			if(irig_data == 3'b111)	next_state = i;
			else 			next_state = z;				
		i:
			next_state = j;
		j:
			if(count == 2)		next_state = k;
			else				next_state = x;				
		k:
			next_state = l;
		l:
			if(~en)			next_state = l;
			else if(en)		next_state = m;
		m:
			if(ind==100)			next_state = n;
			else 				next_state = aa;
		n:
			if(count_fin==val)	next_state = o;
			else 				next_state = n;
		o:
			next_state = b;
		p:
			if(aux==4'b1100)	next_state = r;
			else if(aux==4'b1111)	next_state = q;
			else if(aux<9)		next_state = t;
		q:
			next_state = l;
		r:
			if(irig_data == 3'b111)		next_state = q;
			else						next_state = s;
		s:
			next_state = c;
		t:				
			if(irig_data == 3'b011)			next_state = u;
			else if(irig_data == 3'b001)	next_state = v;				
			else 							next_state = s;
		u:		
			next_state = q;
		v:
			next_state = q;	
		x:
			next_state = e;
		y:
			next_state = g;
                z:
                        next_state = d;
                aa:
                        next_state = p;
				
		default:
			next_state = c;
	endcase
end

always@(posedge clk) begin
	case(actual_state)
		start_state:
			begin			   
			 	start_ = 0;
				terminate_ = 0;
			 	cont_ = 0;
				in_frame_ = 0;
				issue_ = 0;
				rst_reg_ = 1;
				dir_ = 4'b1111;
				write_ = 0;
			end
		a:
		  	begin
				dir_ = 4'b1111;
				rst_reg_ = 0;
			end  
		b:
			begin
				terminate_ = 0;
				rst_reg_ = 0;
			end
		c:
			begin
				start_ = 0;
				rst_reg_ = 1;
				issue_ = 0;	
			end
		d:
			begin
				count = 0; 
				rst_reg_ = 0;
                                issue_ = 0;
			end
		e:
                        begin
                            rst_reg_ = 0;
			    cont_ = 0;
                        end
                f:
                        begin
                            rst_reg_ = 0;
                        end
		i:
			count = count + 1; 
		k:
			begin	
				in_frame_ = 1;
				start_ = 1;
			end
		l:
			begin
				in_frame_ = 0;
				terminate_ = 0;
				issue_ = 0;
				cont_ = 0;
				count_fin = 0;
			end
		n:
			begin
			dir_ = 4'b1111;
			count_fin =count_fin + 1;
			end
		o:
			terminate_ = 1;
		aa:
			aux = dir_dic[ind];//aux = dir_dic[4'd1];
		q:
			begin
				dir_ = 4'b1111;
				in_frame_ = 1;
			end				  
		s:
			begin
				dir_ = 4'b1111;
				issue_ = 1;
			end
		u:
			begin
				dir_ = aux;
				write_ = 1;
			end
		v:
			begin
				dir_ = aux;
				write_ = 0;
			end
		x:
			cont_ = 1;
                z:
                        issue_ = 1;
	endcase
end		 

assign start = start_;
assign terminate = terminate_;
assign dir = dir_;
assign write = write_;
assign rst_reg = rst_reg_;
assign cont = cont_;
assign in_frame = in_frame_;
assign state = actual_state;
assign issue = issue_;
assign aux_out = aux; 

endmodule
