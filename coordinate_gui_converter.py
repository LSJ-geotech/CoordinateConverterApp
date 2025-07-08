import tkinter as tk
from tkinter import filedialog, messagebox
import csv
import os

# 转换度分秒为十进制度（可按需修改）
def dms_to_decimal(dms_str):
    try:
        d, m, s = map(float, dms_str.strip().replace(",", " ").replace("\t", " ").split())
        return d + m / 60 + s / 3600
    except:
        return None

# 主程序类
class CoordinateConverterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("矿点坐标转换工具 v1.0")

        self.label = tk.Label(root, text="请选择包含坐标数据的 TXT 文件")
        self.label.pack(pady=10)

        self.select_button = tk.Button(root, text="选择 TXT 文件", command=self.select_file)
        self.select_button.pack(pady=5)

        self.export_button = tk.Button(root, text="导出为 CSV 文件", command=self.export_csv, state="disabled")
        self.export_button.pack(pady=5)

        self.status_label = tk.Label(root, text="状态：未选择文件")
        self.status_label.pack(pady=10)

        self.filepath = None

    def select_file(self):
        self.filepath = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
        if self.filepath:
            self.status_label.config(text=f"已选择：{os.path.basename(self.filepath)}")
            self.export_button.config(state="normal")

    def export_csv(self):
        output_rows = []
        try:
            with open(self.filepath, "r", encoding="utf-8") as f:
                lines = f.readlines()
                for line in lines:
                    parts = line.strip().split()
                    if len(parts) >= 4:
                        编号 = parts[0]
                        x = dms_to_decimal(parts[1])
                        y = dms_to_decimal(parts[2])
                        备注 = " ".join(parts[3:])
                        if x is not None and y is not None:
                            output_rows.append({"编号": 编号, "X坐标": x, "Y坐标": y, "备注": 备注})

            # 写入CSV文件
            output_path = os.path.splitext(self.filepath)[0] + "_转换结果.csv"
            with open(output_path, "w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=["编号", "X坐标", "Y坐标", "备注"])
                writer.writeheader()
                for row in output_rows:
                    writer.writerow(row)

            self.status_label.config(text=f"✅ 成功导出为：{os.path.basename(output_path)}")
            messagebox.showinfo("完成", "CSV 文件已成功导出！")

        except Exception as e:
            messagebox.showerror("错误", f"处理文件时出错：{str(e)}")

# 运行程序
if __name__ == "__main__":
    root = tk.Tk()
    app = CoordinateConverterApp(root)
    root.mainloop()
