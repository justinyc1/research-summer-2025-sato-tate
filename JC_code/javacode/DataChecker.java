package JC_code.javacode;

public class DataChecker {
    public static void main(String[] args) {
        // validateOutputFileData(new File(FileHelper.outputsDir), 0, 0, 0, 0);
    }

    //     public static void validateOutputFileData(File root, int m_start, int m_end, int d_start, int d_end) {
    //     for (File filename : root.listFiles()) {
    //         if (filename.isDirectory()) {
    //             validateOutputFileData(filename, m_start, m_end, d_start, d_end);
    //         } else {
    //             String[] parts = filename.getName().split("[_.]");
    //             int m = Integer.valueOf(parts[3]);
    //             int d = Integer.valueOf(parts[5]);

    //             for (String s : parts) {
    //                 System.out.print(s + " ");
    //             }
    //             System.out.print("   " + m + "   " + d);
    //             System.out.println();
    //         }
    //     }
    // }
}
