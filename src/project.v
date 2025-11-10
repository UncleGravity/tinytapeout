/*
 * Copyright (c) 2024 Your Name
 * SPDX-License-Identifier: Apache-2.0
 */

`default_nettype none

module tt_um_unclegravity_7seg_counter (
    input  wire [7:0] ui_in,    // Dedicated inputs
    output wire [7:0] uo_out,   // Dedicated outputs
    input  wire [7:0] uio_in,   // IOs: Input path
    output wire [7:0] uio_out,  // IOs: Output path
    output wire [7:0] uio_oe,   // IOs: Enable path (active high: 0=input, 1=output)
    input  wire       ena,      // always 1 when the design is powered, so you can ignore it
    input  wire       clk,      // clock
    input  wire       rst_n     // reset_n - low to reset
);

  // 4-bit counter to count 0-9
  reg [3:0] digit_counter;
  reg [6:0] segments;       // 7-segment display output
  
  // Counter increments on each clock edge (clock is 1Hz from external source)
  always @(posedge clk or negedge rst_n) begin
    if (!rst_n) begin
      digit_counter <= 4'd0;
    end else begin
      // Increment digit counter, wrap at 10
      if (digit_counter == 4'd9) begin
        digit_counter <= 4'd0;
      end else begin
        digit_counter <= digit_counter + 1'd1;
      end
    end
  end
  
  // 7-segment decoder
  // Segments: GFEDCBA (bit 6 down to bit 0)
  //     A
  //   F   B
  //     G
  //   E   C
  //     D
  always @(*) begin
    case (digit_counter)
      4'd0: segments = 7'b0111111;  // 0
      4'd1: segments = 7'b0000110;  // 1
      4'd2: segments = 7'b1011011;  // 2
      4'd3: segments = 7'b1001111;  // 3
      4'd4: segments = 7'b1100110;  // 4
      4'd5: segments = 7'b1101101;  // 5
      4'd6: segments = 7'b1111101;  // 6
      4'd7: segments = 7'b0000111;  // 7
      4'd8: segments = 7'b1111111;  // 8
      4'd9: segments = 7'b1101111;  // 9
      default: segments = 7'b0000000;  // blank
    endcase
  end
  
  // Assign outputs
  // uo_out[6:0] = segments A through G
  // uo_out[7] = decimal point (off)
  assign uo_out = {1'b0, segments};
  
  // Bidirectional pins set as inputs (not used)
  assign uio_out = 8'b0;
  assign uio_oe  = 8'b0;

  // List all unused inputs to prevent warnings
  wire _unused = &{ena, ui_in, uio_in, 1'b0};

endmodule