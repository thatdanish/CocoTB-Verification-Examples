module simple_adder (
    input clk_i,
    input rst_i,
    input data_valid_i,
    input logic [7:0] a,
    input logic [7:0] b,
    input logic [7:0] c,
    output logic [7:0] sum,
    output logic [7:0] carry,
    output logic output_valid_o
);
    always_ff @( posedge clk_i ) begin
        if (!rst_i) begin
            sum <= 'd0;
            carry <= 'd0;
            output_valid_o <= 1'b0;
        end else begin
            if (data_valid_i == 1'b1) begin
                {carry, sum} <= a + b + c;
                output_valid_o <= 1'b1;
            end else begin
                sum <= 'd0;
                carry <= 'd0;
                output_valid_o <= 1'b0;
            end
        end
    end

endmodule