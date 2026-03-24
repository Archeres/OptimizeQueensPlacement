import gurobipy as gp
from gurobipy import GRB

model = gp.Model("Bài toán quân hậu")

# Bàn cờ ban đầu, chưa có bất kỳ quân hậu nào được đặt ra
puzzle = [
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']
]

# addMVar dùng khi tạo một ma trận biến (đôi khi là các biến trong nhiều chiều), 
# shape là kích thước ma trận
n = 8
vars = model.addMVar(shape = (n, n), vtype = GRB.BINARY)

# Ràng buộc của các hàng và cột
for i in range(n):
    model.addConstr(vars[:, i].sum() <= 1) # Mỗi cột tối đa một quân hậu
    model.addConstr(vars[i, :].sum() <= 1) # Mỗi hàng tối đa một quân hậu

# Tưởng tượng bàn cờ là hình vuông ABCD
# A là góc trên bên trái, B là góc trên bên phải, C là góc dưới bên phải, D là góc dưới bên trái

# Ràng buộc đường chéo AC
for k in range (-n + 1, n):
    sumVarsOnAC = 0  
    for i in range(n):
        if (i + k >= 0 and i + k < n):
            sumVarsOnAC += vars[i, i + k] # Cộng các biến x[i, i + k] lại với nhau
    model.addConstr(sumVarsOnAC <= 1) # Đường chéo AC tối đa một quân hậu, tức là tổng các x[i, i + k] trên đường chéo AC phải nhỏ hơn hoặc bằng 1]

# Ràng buộc đường chéo BD
for p in range (0, 2 * n - 2):
    sumVarsOnBD = 0
    for i in range(n):
        if (p - i >= 0 and p - i < n):
            sumVarsOnBD += vars[i, p - i] # Cộng các biến x[i, p - i] lại với nhau
    model.addConstr(sumVarsOnBD <= 1) # Đường chéo BD tối đa một quân hậu, tức là tổng các x[i, p - i] trên đường chéo BD phải nhỏ hơn hoặc bằng 1

model.setObjective(vars.sum(), sense = GRB.MAXIMIZE) # Mục tiêu là đặt được nhiều quân hậu nhất có thể
model.optimize()
print(model.objVal)

# --- GIẢ SỬ ĐOẠN MÃ TRƯỚC ĐÓ ĐÃ CHẠY model.optimize() ---

# Kiểm tra trạng thái của bộ giải (Solver Status)
# model.Status là một số nguyên đại diện cho tình trạng của mô hình sau khi giải.
# GRB.OPTIMAL là một hằng số của Gurobi đại diện cho trạng thái "Đã tìm thấy nghiệm tối ưu".
if model.Status == GRB.OPTIMAL:
    
    # vars.X là một ma trận lấy từ vars (tức các biến ta tạo ra) 
    # trong đó mỗi phần tử là giá trị tối ưu của biến tương ứng sau khi giải mô hình.
    # Ngoài ra, dựa vào vars ta tạo, X sẽ là ma trận khác nhau, ví dụ shape = 3x3 thì X cùng là 3x3
    # ta hiểu rằng X thực tế là bàn cờ sau khi tối ưu, trong đó chỉ chứa các floating point, có dạng:
    # [[0. 0. 0. 1. 0. 0. 0. 0.]
    #  [0. 1. 0. 0. 0. 0. 0. 0.]
    #  [0. 0. 0. 0. 0. 0. 1. 0.]
    #  [0. 0. 1. 0. 0. 0. 0. 0.]
    #  [0. 0. 0. 0. 0. 1. 0. 0.]
    #  [1. 0. 0. 0. 0. 0. 0. 0.]
    #  [0. 0. 0. 0. 0. 0. 0. 1.]
    #  [0. 0. 0. 0. 1. 0. 0. 0.]]
    solution = vars.X # Lưu vào solution để dễ thao tác sau này
    
    # Duyệt qua từng ô bàn cờ
    for i in range(n):
        for j in range(n):
            
            # Kiểm tra xem tại ô (i, j) có đặt quân hậu hay không
            # Giá trị trong 'solution' là số thực (0.0 hoặc 1.0). Do sai số tính toán dấu phẩy động
            # (floating-point error), ta không nên so sánh trực tiếp solution[i, j] == 1.0.
            # Cách an toàn nhất là kiểm tra xem nó có lớn hơn một ngưỡng nhỏ (ví dụ 0.5) hay không.
            if solution[i, j] > 0.5:
                
                # Cập nhật quân hậu vào danh sách puzzle của bạn
                # Ta gán ký tự 'Q' (Queen) vào ô này thay vì khoảng trắng ' '.
                puzzle[i][j] = 'Q'

    # In tiêu đề cho kết quả
    print("\n--- KẾT QUẢ ĐẶT QUÂN HẬU ---")
    
    # In bàn cờ ra màn hình (Terminal)
    # Ta dùng một vòng lặp for để duyệt qua từng hàng (row) trong danh sách puzzle.
    # Mỗi 'row' lúc này là một danh sách nhỏ chứa 8 ký tự.
    for row in puzzle:
        # Lệnh print(row) trong Python sẽ tự động in toàn bộ nội dung của danh sách
        # theo định dạng ['Q', ' ', ' ', ...], giúp bạn nhìn rõ cấu trúc 2 chiều.
        print(row)
        
    print("--------------------------------")

# 8. Xử lý trường hợp không tìm thấy nghiệm
else:
    # Nếu bộ giải báo trạng thái khác (ví dụ: Vô nghiệm - INFEASIBLE), ta in thông báo lỗi.
    print("Mô hình không tìm thấy nghiệm tối ưu hoặc vô nghiệm.")