package JC_code.javacode; // **remove this if this file is NOT in a folder called 'javacode'

//===== libraries that are used for this program =====
import java.util.Set;
import java.util.TreeSet;
import java.util.List;
import java.util.Scanner;
import java.util.HashSet;
import java.util.Iterator;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileWriter;
import java.io.IOException;
import java.io.PrintWriter;
import java.math.BigInteger;
import java.util.ArrayList;
import java.util.Date;
import java.util.HashMap;

public class Project {
    static long startTimeInNano = -1;
    static int maxSecondsAllowed = -1; // in seconds, var <= 0 for no limit
    static boolean skipThisMAndD = false;
    static boolean terminateIfTimeLimit = false;
    static boolean allowOverwrite = false;
    static String generateMethod = ""; // "recursion", "halves"
    static boolean validate_split_in_halves = false;
    static int valid_split_in_half_count = 0;
    static boolean check_tuple_sum = false;
    static int valid_tuple_sum_count = 0;
    static PrintWriter debugOutput = null;
    public static void main(String[] args) throws ProjectException, IOException {
        // test_all_m_and_d_combinations(1246, 1600, 2, 2, false, true, false, -1, false, "halves", false, false);
        // test_all_m_and_d_combinations(51, 51, 11, 15, false, true, false, -1, false, "halves", false, false);
        // test_all_m_and_d_combinations(51, 51, 16, 16, false, true, false, -1, false, "halves", false, false);
        // test_all_m_and_d_combinations(2883, 3600, 2, 2, false, true, false, -1, false, "halves", false, false);
        // test_all_m_and_d_combinations(49, 49, 11, 999, false, true, false, -1, false, "halves", false, false);

        // test_all_m_and_d_combinations(49, 49, 11, 999, true, true, true, -1, false, "halves", false, false);

        test_all_m_and_d_combinations(63, 100, 1, 999, true, true, true, 1800, false, "halves", false, false); // 30 minutes "soft" limit (if reached, finish current then skip)
    }

    public static void test_all_m_and_d_combinations(int m_start, int m_end, int d_start, int d_end, boolean print_outputs, boolean automated, boolean overwrite_outputs, int max_seconds_allowed, boolean terminate_if_time_limit, String generate_method, boolean validate_halves, boolean check_sum) throws IOException {
        allowOverwrite = overwrite_outputs;
        maxSecondsAllowed = max_seconds_allowed;
        generateMethod = generate_method;
        validate_split_in_halves = validate_halves;
        check_tuple_sum = check_sum;
        Scanner sc = new Scanner(System.in);
        if (!automated) System.out.println("Press the Enter Key to process the next m and d values");
        sc.useDelimiter("\r"); // a single enter press is now the separator.
        for (int i = m_start; i <= m_end; ++i) {
            if (i % 2 == 0) continue;
            // if (i % 3 != 0) continue; //DEBUG m=3q
            int d_limit = (i-1)/2;
            int jSkipToValue = -1;
            for (int j = d_start; j <= d_limit && j <= d_end; ++j) {
                FileHelper.deleteAllEmptyFiles(new File(FileHelper.outputsDir)); // delete empty files
                if (skipThisMAndD) {
                    System.out.printf("Previous iteration with m = %d, d = %d exceeded the %d second%s time limit.\n", i, j-1, max_seconds_allowed, plural(max_seconds_allowed));
                    jSkipToValue = d_limit - j;
                    skipThisMAndD = false;
                }
                if (j <= jSkipToValue + 1) {
                    System.out.println("Skipping at m = " + i + ", d = " + j);
                    continue;
                }
                System.out.println("Starting time for m = " + i + ", d = " + j + " is " + new Date());
                try {
                    System.gc(); // free up memory
                    validate_set_V(i, j, print_outputs);
                } catch (ProjectException e) {
                    continue;
                }
                System.out.println("Ending time for m = " + i + ", d = " + j + " is " + new Date());
                if (!automated) sc.next();
            } 
        }
        sc.close();
    }

    public static void validate_set_V(int m, int d) throws ProjectException, IOException {
        validate_set_V(m, d, false);
    }

    /**
     * TODO: possibly rename the method to a more meaningful name
     * @param m - An positve odd integer
     * @param d - An positive integer in the range: 1 <= d <= (m-1)/2
     */
    public static void validate_set_V(int m, int d, boolean print_outputs) throws ProjectException, IOException {
        System.out.println("Running method validate_set_V(" + redString("m = ", m) + ", " + redString("d = ", d) + ") and generating using " + generateMethod + ":\n");
        
        validate_m_and_d(m, d);

        String filepath = "JC_code\\outputs\\";
        String filename = "m_" + m + "\\output_for_m_" + m + "_d_" + d + ".txt";
        File currentFile = new File(filepath + filename);

        // if allowing printing outputs IS allowed but overwriting existing output files IS NOT allowed, exception will be thrown for this m, d
        if (print_outputs && !allowOverwrite && currentFile.exists() && !currentFile.isDirectory()) {
            throw new ProjectException("overwrite_outputs disabled and printing to file enabled, while file for m = " + m + ", d = " + d + " already exists.");
        }

        PrintWriter pw = new PrintWriter(filepath + "\\.misc\\default_output.txt"); // default output file
        if (print_outputs) {
            pw = new PrintWriter(currentFile);
        }

        long startTime = System.nanoTime();
        startTimeInNano = startTime;

        //===== create and put valid values in 'Z/mZ' and 'Z/mZ*' set =====
        Set<Integer> Z_mod_m_Z = new HashSet<>();
        Set<Integer> Z_mod_m_Z_star = new HashSet<>();
        generate_ZmmZ_and_ZmmZs(m, Z_mod_m_Z, Z_mod_m_Z_star);

        // Set<Tuple> U_set = new HashSet<>(); // contains all alpha tuples that are valid for the U set
        // Set<Tuple> B_set = new HashSet<>(); // contains all alpha tuples that are valid for the B set
        Set<Tuple> V_set = new HashSet<>(); // contains all tuples from the B set that are valid for the V set
        find_all_valid_alpha_combinations(V_set, Z_mod_m_Z_star, m, d);

        //TODO: can we find pairs by indices? i.e. a_i and a_(n-i) are pairs or there are no pairs
        /* Exceptional Cycles:
         *   an exceptional cycle is a tuple that is not coming exclusively from pairs that add to m
         *   example: for tuple (1,4,6,7), it does not contain exclusively pairs that add to m, in fact there are no pairs that add to m at all
         *   thus: a tuple is an exceptional cycle if it is not only pairs of elements that add to m; if there is at least 1 value that don't have a pair, then it is not an exceptional cycle
         * 
         *   guess: if m is prime, there are no exceptional cycles
         */
        
        Set<Tuple> all_are_pairs = new HashSet<>();  // contains all tuples from the V set that have  ONLY PAIRS  adding up to m
        Set<Tuple> some_are_pairs = new HashSet<>(); // contains all tuples from the V set that have  SOME PAIRS  adding up to m (but not all pairs)
        Set<Tuple> none_are_pairs = new HashSet<>(); // contains all tuples from the V set that have  NO PAIRS    adding up to m
        Set<Tuple> indecomposable = new HashSet<>(); // contains all tuples from the V set that have  NO SUBSETS  adding up to m
        Set<Tuple> decomposable_but_no_pairs = new HashSet<>(); // contains all tuples from the V set that HAVE SUBSETS & NO PAIRS  adding up to m
        Set<Tuple> exceptional_cycles = new HashSet<>(); // contains all tuples from the V set that are not made up of exclusively pairs
        // TODO: check code for indecomposable; check indecomposable definitions
        populate_all_some_none_exceptional_sets(V_set, m, all_are_pairs, some_are_pairs, none_are_pairs, exceptional_cycles);

        StringBuilder no_pair_print_buffer = new StringBuilder();
        // ===== indecomposable set and decomposable but no pairs set =====
        populate_indecomposable_and_decomposable_but_no_pairs_sets(m, d, none_are_pairs, indecomposable, decomposable_but_no_pairs, print_outputs, no_pair_print_buffer);

        long endTime = System.nanoTime();
        String formattedElapsedTime = get_formatted_elapsed_time(startTime, endTime);

        // System.out.println("\nPrint \"reduced\" " + redString("U") + " set (contains " + redString(U_set.size()) + " tuples): " + U_set); //DEBUG
        // System.out.println("\nPrint \"reduced\" " + redString("B") + " set (contains " + redString(B_set.size()) + " tuples): " + B_set); //DEBUG
        // System.out.println("\nPrint " + redString("V") + " set (contains " + redString(V_set.size()) + " tuples): " + V_set); //DEBUG
        // System.out.println("\nPrint " + redString("all") + "_are_pairs" + " (contains " + redString(all_are_pairs.size()) + " tuples): " + all_are_pairs); //DEBUG
        // System.out.println("\nPrint " + redString("some") + "_are_pairs" + " (contains " + redString(some_are_pairs.size()) + " tuples): " + some_are_pairs); //DEBUG
        // System.out.println("\nPrint " + redString("none") + "_are_pairs" + " (contains " + redString(none_are_pairs.size()) + " tuples): " + none_are_pairs); //DEBUG
        // System.out.println("\nPrint " + redString("indecomposable") + " (contains " + redString(indecomposable.size()) + " tuples): " + indecomposable); //DEBUG
        // System.out.println("\nPrint " + redString("decomposable but no pairs") + " (contains " + redString(decomposable_but_no_pairs.size()) + " tuples): " + decomposable_but_no_pairs); //DEBUG
        // System.out.println("\nPrint " + redString("exceptional") + " cycles (contains " + redString(exceptional_cycles.size()) + " tuples): " + exceptional_cycles); //DEBUG
        System.out.println();

        // extra summary section (using space for spacing/aligning instead of printf)
        System.out.println("Summary:");
        System.out.println("given " + redString("m = ", m) + ", " + redString("d = ", d));
        System.out.println("Calculations took " + formattedElapsedTime + ".");
        System.out.println("All " + redString("ascending & non-repeating") + " tuple (" + redString("size ", 2*d) + ") combinations possible for the U set: " + find_num_of_ascending_nonrepeating_tuples_in_U_set(Z_mod_m_Z, d));
        // System.out.println("All " + redString("ascending & non-repeating") + " tuple (" + redString("size 1 to ", 2*d) + ") combinations possible for the U set: " + (new BigInteger("2").pow(Z_mod_m_Z.size()-1).subtract(BigInteger.ONE)));
        // System.out.println("            " +"\"reduced\" " + redString("U") + " set: contains " + redString(U_set.size()) + " tuples");
        // System.out.println("            " + "\"reduced\" " + redString("B") + " set: contains " + redString(B_set.size()) + " tuples");
        System.out.println("                      " + redString("V") + " set: contains " + redString(V_set.size()) + " tuples");
        System.out.println("          " + redString("all") + "_are_pairs" + " set: contains " + redString(all_are_pairs.size()) + " tuples");
        // System.out.println("         " + redString("some") + "_are_pairs" + " set: contains " + redString(some_are_pairs.size()) + " tuples");
        System.out.println("         " + redString("none") + "_are_pairs" + " set: contains " + redString(none_are_pairs.size()) + " tuples");
        System.out.println("         " + redString("indecomposable") + " set: contains " + redString(indecomposable.size()) + " tuples");
        // System.out.println(redString("decomposable & no pairs") + " set: contains " + redString(decomposable_but_no_pairs.size()) + " tuples");
        System.out.println("     " + redString("exceptional") + "_cycles" + " set: contains " + redString(exceptional_cycles.size()) + " tuples");

        if (print_outputs) pw.println("Running method validate_set_V(m = " + m + ", d = " + d + ") and generating using " + generateMethod + ":\n");
        if (print_outputs) pw.println("Summary:");
        if (print_outputs) pw.println("given m = " + m + ", d = " + d);
        if (print_outputs) pw.println("Calculations took " + formattedElapsedTime + ".");
        if (print_outputs) pw.println("Z/mZ:  " + Z_mod_m_Z.toString());
        if (print_outputs) pw.println("Z/mZ*: " + Z_mod_m_Z_star.toString());
        if (print_outputs) pw.println("All ascending & non-repeating tuple (size " + 2*d + ") combinations possible for the U set: " + find_num_of_ascending_nonrepeating_tuples_in_U_set(Z_mod_m_Z, d));
        // if (print_outputs) pw.println("All ascending & non-repeating tuple (size 1 to " + 2*d + ") combinations possible for the U set: " + (new BigInteger("2").pow(Z_mod_m_Z.size()-1).subtract(BigInteger.ONE)));
        // if (print_outputs) pw.println("            " +"\"reduced\" U set: contains " + U_set.size() + " tuples");
        // if (print_outputs) pw.println("            \"reduced\" B set: contains " + B_set.size() + " tuples");
        if (print_outputs) pw.println("                      V set: contains " + V_set.size() + " tuples");
        if (print_outputs) pw.println("          all_are_pairs set: contains " + all_are_pairs.size() + " tuples");
        if (print_outputs) pw.println("         some_are_pairs set: contains " + some_are_pairs.size() + " tuples");
        if (print_outputs) pw.println("         none_are_pairs set: contains " + none_are_pairs.size() + " tuples");
        if (print_outputs) pw.println("         indecomposable set: contains " + indecomposable.size() + " tuples");
        if (print_outputs) pw.println("decomposable & no pairs set: contains " + decomposable_but_no_pairs.size() + " tuples");
        if (print_outputs) pw.println("     exceptional_cycles set: contains " + exceptional_cycles.size() + " tuples");

        // if (print_outputs) pw.println("Print \"reduced\" U set (contains " + U_set.size() + " tuples): " + toStringSorted(U_set, "\n")); //DEBUG
        // if (print_outputs) pw.println("Print \"reduced\" B set (contains " + B_set.size() + " tuples): " + toString(B_set, "\n")); //DEBUG
        if (print_outputs && V_set.size() <= 10000) pw.println("\nPrint V set (contains " + V_set.size() + " tuples): " + toStringSorted(V_set, "\n")); //DEBUG
        if (print_outputs && all_are_pairs.size() <= 10000) pw.println("\nPrint all_are_pairs (contains " + all_are_pairs.size() + " tuples): " + toString(all_are_pairs, "\n")); //DEBUG
        if (print_outputs && some_are_pairs.size() <= 10000) pw.println("\nPrint some_are_pairs (contains " + some_are_pairs.size() + " tuples): " + toString(some_are_pairs, "\n")); //DEBUG
        if (print_outputs && none_are_pairs.size() <= 20000) pw.println("\nPrint none_are_pairs (contains " + none_are_pairs.size() + " tuples): " + toString(none_are_pairs, "\n")); //DEBUG
        if (print_outputs && indecomposable.size() <= 20000) pw.println("\nPrint indecomposable (contains " + indecomposable.size() + " tuples): " + toString(indecomposable, "\n")); //DEBUG
        if (print_outputs && decomposable_but_no_pairs.size() <= 20000) pw.println("\nPrint decomposable but no pairs (contains " + decomposable_but_no_pairs.size() + " tuples): " + toString(decomposable_but_no_pairs, "\n")); //DEBUG
        if (print_outputs && exceptional_cycles.size() <= 20000) pw.println("\nPrint exceptional cycles (contains " + exceptional_cycles.size() + " tuples): " + toString(exceptional_cycles, "\n")); //DEBUG
        // if (print_outputs) pw.println("\nBelow are debug outputs for each alpha in V whether it was put in the indecomposable set or the decomposable but no pairs set:");
        // if (print_outputs && no_pair_print_buffer.length() <= 200000) pw.println(no_pair_print_buffer.toString());

        PrintWriter historyLog = new PrintWriter(new FileWriter("JC_code\\outputs\\.misc\\" + "log.txt", true));
        historyLog.println("Summary:");
        historyLog.println("given m = " + m + ", d = " + d);
        historyLog.println("Calculations took " + formattedElapsedTime + ".");
        historyLog.println("All ascending & non-repeating tuple (size " + 2*d + ") combinations possible for the U set: " + find_num_of_ascending_nonrepeating_tuples_in_U_set(Z_mod_m_Z, d));
        historyLog.println("                      V set: contains " + V_set.size() + " tuples");
        historyLog.println("          all_are_pairs set: contains " + all_are_pairs.size() + " tuples");
        // historyLog.println("         some_are_pairs set: contains " + some_are_pairs.size() + " tuples");
        historyLog.println("         none_are_pairs set: contains " + none_are_pairs.size() + " tuples");
        historyLog.println("         indecomposable set: contains " + indecomposable.size() + " tuples");
        // historyLog.println("decomposable & no pairs set: contains " + decomposable_but_no_pairs.size() + " tuples");
        historyLog.println("     exceptional_cycles set: contains " + exceptional_cycles.size() + " tuples");
        if ((exceptional_cycles.size()+1) * 3 != m) historyLog.println("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"); //DEBUG
        historyLog.println();
        historyLog.close();

        if ((exceptional_cycles.size()+1) * 3 != m) System.out.println("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"); //DEBUG
        System.out.println("\nmethod validate_set_V(" + redString(m) + ", " + redString(d) + ") ran to completion.");
        if (print_outputs) pw.println("\nmethod validate_set_V(" + m + ", " + d + ") ran to completion.");

        pw.close();
        return;
    }

    /** Makes sure m and d are valid 
     * 
     * @param m where m is: odd, or equal to p*q (where p and q are different primes), or equal to p^n where n >= 2
     * @param d where d is in the range: 1 <= d <= (m-1)/2
     * @throws ProjectException if m or d is invalid
     */
    public static void validate_m_and_d(int m, int d) throws ProjectException {
        if (m % 2 == 0) throw new ProjectException("m is not odd: m = " + m);
        if (d < 1) throw new ProjectException("d is not greater than or equal to 1: d = " + d);
        if (d > (m-1)/2) throw new ProjectException("d is not less than or equal to (m-1)/2: d = " + d + ", (m-1)/2 = " + (m-1)/2);
    }

    public static void generate_ZmmZ_and_ZmmZs(int m, Set<Integer> Z_mod_m_Z, Set<Integer> Z_mod_m_Z_star) {
        for (int i = 0; i < m; ++i) {
            Z_mod_m_Z.add(i);
            if (gcd(i, m) == 1) {
                Z_mod_m_Z_star.add(i);
            }
        }
    }

    /** Calls the recursive algorithm to find all valid ascending combinations of alpha tuple
     * 
     * @param V_set
     * @param m - the upper limit (exclusive) of Z/mZ when finding combinations
     * @param alpha_length - length of each alpha tuple, determined by n
     * @throws IOException 
     */
    public static void find_all_valid_alpha_combinations(Set<Tuple> V_set, Set<Integer> ZmmZ_star, int m, int d) throws ProjectException, IOException {
        int alpha_length = 2 * d;
        int[] this_combination = new int[alpha_length];
        if (validate_split_in_halves || check_tuple_sum) {
            debugOutput = new PrintWriter(new FileWriter("JC_code\\outputs\\.misc\\" + "debug_output.txt", true));
            recursively_find_all_check_info(V_set, ZmmZ_star, m, this_combination, 0, 1, (alpha_length-2)/2+1);
            debugOutput.close();
        } else {
            if (generateMethod == "recursion") { // original recursive implementation
                find_all_recursively(V_set, ZmmZ_star, m, this_combination, 0, 1, (alpha_length-2)/2+1);
            } else if (generateMethod == "halves") { // newer, generate using half-tuples
                find_all_using_halves(V_set, ZmmZ_star, m, alpha_length, (alpha_length-2)/2+1);
            } else { // default: generate using halves
                find_all_using_halves(V_set, ZmmZ_star, m, alpha_length, (alpha_length-2)/2+1);
            }
        }
    }

    private static void find_all_using_halves(Set<Tuple> V_set, Set<Integer> ZmmZ_star, int m, int alpha_length, int n_halved_plus_one) throws ProjectException, IOException {
        int d = alpha_length/2;
        int m_minus_one_divided_by_two = (m-1)/2;
        // int m_choose_d = Integer.valueOf(nCr(BigInteger.valueOf(m), BigInteger.valueOf(d)).toString());
        int hold = 10;
        ArrayList<Tuple> firstHalves = new ArrayList<>(hold);
        HashMap<Integer, ArrayList<Tuple>> inversed_sum_tuples_map = new HashMap<>(hold);
        int[] this_combination = new int[d];
        find_halves_recursively(firstHalves, inversed_sum_tuples_map, m, m_minus_one_divided_by_two, this_combination, 0, 1);
        
        // PrintWriter pwTesting = new PrintWriter("JC_code\\outputs\\.misc\\testing.txt"); // TESTING

        // pwTesting.println(firstHalves.size() + " " + inversed_sum_tuples_map.size()); // TESTING
        for (int i = 0; i < firstHalves.size(); i++) {
            Tuple curr = firstHalves.get(i);
            int sum = curr.sum();
            if (!inversed_sum_tuples_map.containsKey(sum)) {
                // pwTesting.println("HASHMAP DOES NOT CONTAIN THE KEY: SUM = " + sum + " !!!"); // TESTING
                continue;
            }
            int left = curr.get(curr.size()-1);
            for (Tuple alpha : inversed_sum_tuples_map.get(sum)) {
                if (left == alpha.get(alpha.size()-1)) {
                    // pwTesting.println("END OF FIRST HALF = START OF SECOND HALF ???"); // TESTING
                    continue;
                }
                put_in_V_set_if_valid(V_set, ZmmZ_star, curr.merge(alpha), m, n_halved_plus_one);
            }
        }
        // pwTesting.println(V_set.size()); // TESTING

        // pwTesting.close(); // TESTING
    }
    
    /* Thoughts for a possibly better recursive implementation 
     *
     * while first element is valid:
     *   if list is "full" OR last element == max for that index:
     *     pop
     *   else:
     *     get prev element
     *       put prev+1 into next element
     *       if this combination is size k and valid
     *         add to set
     */
    private static void find_halves_recursively(ArrayList<Tuple> firstHalves, HashMap<Integer, ArrayList<Tuple>> inversed_sum_tuples_map, int m, int m_minus_one_divided_by_two, int[] this_combination, int sum, int depth) {
        if (depth > this_combination.length) {
            return;
        }
        
        int prev = 0;
        if (depth > 1) prev = this_combination[depth-2];
        for (int i = Integer.max(depth, prev + 1); i <= m_minus_one_divided_by_two - this_combination.length + depth; ++i) {
            this_combination[depth-1] = i;
            sum += i;

            if (depth == this_combination.length) {
                Tuple this_tuple = new Tuple(this_combination);
                firstHalves.add(this_tuple);

                if (!inversed_sum_tuples_map.containsKey(sum)) {
                    ArrayList<Tuple> emptyList = new ArrayList<>();
                    inversed_sum_tuples_map.put(sum, emptyList);
                }
                inversed_sum_tuples_map.get(sum).add(this_tuple.inverse(m));
            }
            
            find_halves_recursively(firstHalves, inversed_sum_tuples_map, m, m_minus_one_divided_by_two, this_combination, sum, depth+1);
            
            sum -= i;
        }
    }

    /** Recursively find all valid ascending combinations of alpha tuple, using the values of Z/mZ (excluding 0)
     * 
     * @param V_set
     * @param m 
     * @param this_combination - an array that contains all the elements in the alpha tuple for the current loop
     * @param sum - stores the sum of the elements in this_combination
     * @param depth - the current level of the recursion method
     */
    private static void find_all_recursively(Set<Tuple> V_set, Set<Integer> ZmmZ_star, int m, int[] this_combination, int sum, int depth, int n_halved_plus_one) throws ProjectException {
        if (depth > this_combination.length) {
            // System.out.println("depth = " + depth + "   returning"); // DEBUG
            return;
        }
        
        int prev = 0;
        if (depth > 1) prev = this_combination[depth-2];
        // System.out.println("for comb " + toString(this_combination) + " the prev is " + prev); // DEBUG
        for (int i = Integer.max(depth, prev + 1); i <= m - 1 - this_combination.length + depth; ++i) {
            // if (depth == 1) System.out.println((this_combination[0]+1) + " out of " + (m-this_combination.length)); // DEBUG 
            this_combination[depth-1] = i;
            sum += i;

            // System.out.println(toString(this_combination, depth) + "   depth = " + depth + "   sum: " + sum); // DEBUG

            // if (this_combination.size() == alpha_length) System.out.println(this_combination.toString() + "   sum: " + sum); //DEBUG
            if (depth == this_combination.length && sum % m == 0) {
                // V_set.add(new Tuple(this_combination));
                put_in_V_set_if_valid(V_set, ZmmZ_star, this_combination, m, n_halved_plus_one);
            }
            
            find_all_recursively(V_set, ZmmZ_star, m, this_combination, sum, depth+1, n_halved_plus_one);
            
            // System.out.print("subtracting from sum = " + sum + " by last element at index " + depth + "-1 = " + this_combination[depth-1]); // DEBUG
            // sum -= this_combination[depth-1];
            sum -= i;
            // System.out.println("   sum is now = " + sum); // DEBUG
            // this_combination[depth-1] = 0; // dont need to be removed, but could get garbage values based on implementation
        }
    }

    private static void recursively_find_all_check_info(Set<Tuple> V_set, Set<Integer> ZmmZ_star, int m, int[] this_combination, int sum, int depth, int n_halved_plus_one) throws ProjectException, FileNotFoundException {
        if (depth > this_combination.length) {
            return;
        }
        
        int prev = 0;
        if (depth > 1) prev = this_combination[depth-2];
        for (int i = Integer.max(depth, prev + 1); i <= m - 1 - this_combination.length + depth; ++i) {
            this_combination[depth-1] = i;
            sum += i;

            if (depth == this_combination.length && sum % m == 0) {
                put_in_V_set_if_valid_and_check_info(V_set, ZmmZ_star, this_combination, m, n_halved_plus_one);
            }
            
            recursively_find_all_check_info(V_set, ZmmZ_star, m, this_combination, sum, depth+1, n_halved_plus_one);
            sum -= i;
        }
    }

    public static void put_in_V_set_if_valid(Set<Tuple> V_set, Set<Integer> Z_mod_m_Z_star, int[] alpha, int m, int n_halved_plus_one) throws ProjectException {
        if (maxSecondsAllowed > 0) { // has time limit
            terminate_if_longer_than_n_seconds(maxSecondsAllowed);
        }
        boolean this_alpha_is_valid = true;
        // System.out.println(n_halved_plus_one);
        for (int t : Z_mod_m_Z_star) {

            List<Integer> t_times_alpha_reduced_elements = new ArrayList<>();
            double t_times_alpha_reduced_sum = 0;

            for (int i = 0; i < alpha.length; ++i) {
                int reduced_mod_m = (t * alpha[i]) % m;
                t_times_alpha_reduced_elements.add(reduced_mod_m);
                t_times_alpha_reduced_sum += reduced_mod_m;
            }
            t_times_alpha_reduced_sum /= m;

            // System.out.println("for tuple " + alpha + " and t = " + t + ", t*a = " + t_times_alpha_reduced_elements + " and |t*a| = " + t_times_alpha_reduced_sum);//DEBUG
            // System.out.printf("for tuple %-16s and t = %2d, t*a = %-16s and |t*a| = %1.0f\n", alpha.toString(), t, t_times_alpha_reduced_elements.toString(), t_times_alpha_reduced_sum);//DEBUG
            if (t_times_alpha_reduced_sum != n_halved_plus_one) {
                this_alpha_is_valid = false;
                break; // if |t * alpha| != n/2 +1 for just one t, this alpha tuple is not valid for the B set
            }
        }
        if (this_alpha_is_valid) {
            // B_set.add(alpha);
            V_set.add(new Tuple(alpha));
        }
    }

    public static void put_in_V_set_if_valid(Set<Tuple> V_set, Set<Integer> Z_mod_m_Z_star, Tuple alpha, int m, int n_halved_plus_one) throws ProjectException {
        if (maxSecondsAllowed > 0) { // has time limit
            terminate_if_longer_than_n_seconds(maxSecondsAllowed);
        }
        boolean this_alpha_is_valid = true;
        // System.out.println(n_halved_plus_one);
        for (int t : Z_mod_m_Z_star) {

            List<Integer> t_times_alpha_reduced_elements = new ArrayList<>();
            double t_times_alpha_reduced_sum = 0;

            for (int i = 0; i < alpha.size(); ++i) {
                int reduced_mod_m = (t * alpha.get(i)) % m;
                t_times_alpha_reduced_elements.add(reduced_mod_m);
                t_times_alpha_reduced_sum += reduced_mod_m;
            }
            t_times_alpha_reduced_sum /= m;

            // System.out.println("for tuple " + alpha + " and t = " + t + ", t*a = " + t_times_alpha_reduced_elements + " and |t*a| = " + t_times_alpha_reduced_sum);//DEBUG
            // System.out.printf("for tuple %-16s and t = %2d, t*a = %-16s and |t*a| = %1.0f\n", alpha.toString(), t, t_times_alpha_reduced_elements.toString(), t_times_alpha_reduced_sum);//DEBUG
            if (t_times_alpha_reduced_sum != n_halved_plus_one) {
                this_alpha_is_valid = false;
                break; // if |t * alpha| != n/2 +1 for just one t, this alpha tuple is not valid for the B set
            }
        }
        if (this_alpha_is_valid) {
            // B_set.add(alpha);
            V_set.add(alpha);
        }
    }

    public static void put_in_V_set_if_valid_and_check_info(Set<Tuple> V_set, Set<Integer> Z_mod_m_Z_star, int[] alpha, int m, int n_halved_plus_one) throws ProjectException {
        if (maxSecondsAllowed > 0) { // has time limit
            terminate_if_longer_than_n_seconds(maxSecondsAllowed);
        }
        boolean this_alpha_is_valid = true;
        // System.out.println(n_halved_plus_one);
        for (int t : Z_mod_m_Z_star) {

            List<Integer> t_times_alpha_reduced_elements = new ArrayList<>();
            double t_times_alpha_reduced_sum = 0;

            for (int i = 0; i < alpha.length; ++i) {
                int reduced_mod_m = (t * alpha[i]) % m;
                t_times_alpha_reduced_elements.add(reduced_mod_m);
                t_times_alpha_reduced_sum += reduced_mod_m;
            }
            t_times_alpha_reduced_sum /= m;

            // System.out.println("for tuple " + alpha + " and t = " + t + ", t*a = " + t_times_alpha_reduced_elements + " and |t*a| = " + t_times_alpha_reduced_sum);//DEBUG
            // System.out.printf("for tuple %-16s and t = %2d, t*a = %-16s and |t*a| = %1.0f\n", alpha.toString(), t, t_times_alpha_reduced_elements.toString(), t_times_alpha_reduced_sum);//DEBUG
            if (t_times_alpha_reduced_sum != n_halved_plus_one) {
                this_alpha_is_valid = false;
                break; // if |t * alpha| != n/2 +1 for just one t, this alpha tuple is not valid for the B set
            }
        }
        if (this_alpha_is_valid) {
            // B_set.add(alpha);
            if (validate_split_in_halves) validate_split_halves(alpha, m); // DEBUG
            if (check_tuple_sum) validate_tuple_sum(alpha, m); //
            V_set.add(new Tuple(alpha));
        }
    }

    public static void validate_tuple_sum(int[] tuple_array, int m) throws ProjectException {
        int sum = sumOf(tuple_array);
        int d = tuple_array.length / 2;
        int m_times_d = m * d;
        if (sum == m_times_d) { // normal
            valid_tuple_sum_count++;
            if (valid_tuple_sum_count % 1000 == 0) {
                System.out.println(valid_tuple_sum_count + " tuples checked are valid halves.");
            }
        } else { // anomaly
            System.out.printf("For m = %d, d = %d, the tuple %s with sum %d does not equal m*d = %d, after %d normal combinations in a row.\n", m, tuple_array.length, toString(tuple_array), sum, m_times_d, valid_tuple_sum_count);
            debugOutput.append(String.format("\nFor m = %d, d = %d, the tuple in U set %s with sum %d does not equal m*d = %d, after %d normal combinations in a row.\n", m, tuple_array.length, toString(tuple_array), sum, m_times_d, valid_tuple_sum_count));
            valid_tuple_sum_count = 0;
        }
    }

    public static void validate_split_halves(int[] tuple_array, int m) throws ProjectException {
        int n = tuple_array.length;
        int m_minus_one_divided_by_two = (m-1)/2;
        int invalid_index = -1;
        for (int j = 0; j < n; j++) {
            if (j < n/2) { // left half
                if (tuple_array[j] > m_minus_one_divided_by_two) {
                    invalid_index = j;
                    break;
                }
            } else { // right half
                if (tuple_array[j] < m_minus_one_divided_by_two) {
                    invalid_index = j;
                    break;
                }
            }
        }
        if (invalid_index == -1) { // normal
            valid_split_in_half_count++;
            if (valid_split_in_half_count % 1000 == 0) {
                System.out.println(valid_split_in_half_count + " tuples checked are valid halves.");
            }
        } else { // anomaly
            System.out.printf("For m = %d, d = %d, the tuple %s at index %d violates the two halves observation, after %d normal combinations in a row.\n", m, tuple_array.length, toString(tuple_array), invalid_index, valid_split_in_half_count);
            debugOutput.append(String.format("\nFor m = %d, d = %d, the tuple in U set %s at index %d violates the two halves observation, after %d normal combinations in a row.\n", m, tuple_array.length, toString(tuple_array), invalid_index, valid_split_in_half_count));
            valid_split_in_half_count = 0;
        }
    }

    public static void populate_all_some_none_exceptional_sets(Set<Tuple> V_set, int m, Set<Tuple> all_are_pairs, Set<Tuple> some_are_pairs, Set<Tuple> none_are_pairs, Set<Tuple> exceptional_cycles) {
        // TODO: should be a way to make this faster? (actually prob not)
        for (Tuple tuple : V_set) { // for each tuple
            // System.out.println("for tuple " + tuple); //DEBUG

            // some boolean variables to keep track of each tuple's traits
            boolean has_all_pairs = true;  // assume true, if any element don't have a pair, set to false
            boolean has_one_pair = false; // assume false, if any element have a pair, set to true
            boolean has_no_pairs = true;   // assume true, if any element have a pair, set to false
            // TODO: has_one_pair and has_all_pair are inverses; A = B'

            for (int i = 0; i < tuple.size(); ++i) { // for an element at i of tuple
                boolean ith_element_has_pair = false;

                // for any element at i, j loop makes sure to set ith_element_has_pair to true if found a pair, or ith_element_has_pair remains false, which means the tuple is an exceptional cycle
                for (int j = 0; j < tuple.size(); ++j) { // check every element (as j)
                    // System.out.print("  at i: " + tuple.get(i) + "  at j: " + tuple.get(j) + "  and m = " + m); //DEBUG
                    if ((tuple.get(i) + tuple.get(j)) % m == 0) {
                        // System.out.println("   PAIR FOUND"); //DEBUG
                        ith_element_has_pair = true;
                        break;
                    }
                    // System.out.println();
                }

                if (ith_element_has_pair) { // if just one element has a pair then
                    has_no_pairs = false; 
                    has_one_pair = true; // we assume theres at least one pair
                } else { // an element don't have a pair
                    has_all_pairs = false;
                }

            }

            if (has_all_pairs) { // has_all_pairs remains true if every element has a pair
                all_are_pairs.add(tuple);
            } else { // not every element have a pair:
                exceptional_cycles.add(tuple);
                if (has_one_pair) { // if there is at least one pair (but not all elements are pairs) then SOME elements are pairs
                    some_are_pairs.add(tuple);
                } else if (has_no_pairs) { // if no pairs but has subsets, then only add to the no pairs set
                    none_are_pairs.add(tuple);
                }
            }
        }
    }

    public static void populate_indecomposable_and_decomposable_but_no_pairs_sets(int m, int d, Set<Tuple> none_are_pairs, Set<Tuple> indecomposable, Set<Tuple> decomposable_but_no_pairs, boolean print_outputs, StringBuilder no_pair_print_buffer) throws ProjectException {
        int min_subset_size = 4;
        int max_subset_size = 2 * d - 2;

        // ===== indecomposable set and decomposable but no pairs set =====
        // when d = 1,2 (d=1 => 2 elements = all pairs, d=2 => both pairs or no pairs)
        // TODO: for d >= 3, check subtuples of 'half size' instead of full size (?)
        if (d == 2) {
            for (Tuple alpha : none_are_pairs) {
                // if the first element have a pair, then the other two numbers are also pairs.
                if (alpha.get(0) + alpha.get(1) == m || 
                    alpha.get(0) + alpha.get(2) == m || 
                    alpha.get(0) + alpha.get(3) == m
                ) {
                    continue;
                }
                // else there is no pairs in alpha. when d = 2, only alpha_1 and alpha_2 would be pairs. therefore at this point it is indecomposable
                if (print_outputs) no_pair_print_buffer.append("adding to indecomposable set: " + alpha + "\n");
                indecomposable.add(alpha);
            }
        }
        if (d >= 3) { // when d = 2 or less, alpha have at most 4 elements, so there is no indecomposables nor decomposable but no pairs 
            for (Tuple alpha : none_are_pairs) { // each element is an alpha with no pairs
                boolean divides_m = false;
                Tuple subtuple = Tuple.EMPTY_TUPLE;
                for (int size = min_subset_size; size <= max_subset_size; size+=2) { // for each possible subtuple length:
                    // go though each possible subtuple combination from alpha to find a subtuple that adds to multiple of m

                    // init subtuple
                    subtuple = alpha.getSubtuple(0, size);
                    // System.out.println("For tuple " + alpha + ", check subtuple " + subtuple);

                    // check init values divides m
                    if (subtuple.sum() % m == 0) {
                        divides_m = true;
                        break;
                    }

                    // check every subset combinations if they divides m
                    while (subtuple != null) {
                        if (subtuple.sum() % m == 0) {
                            // System.out.println("for " + alpha + ", the subtuple " + subtuple + " divides m = " + m); // DEBUG
                            divides_m = true;
                            break;
                        }
                        subtuple = alpha.getNextAscendingTupleAfter(subtuple);
                        // System.out.println("For tuple " + alpha + ", check subtuple " + subtuple);
                    }

                    if (divides_m) break;
                }
            // back to for each alpha
                if (divides_m) {
                    // System.out.println("adding to decomposable but no pairs set: " + alpha + ", since subtuple = " + subtuple);
                    // if (print_outputs) pw.println("adding to decomposable but no pairs set: " + alpha);
                    if (print_outputs) no_pair_print_buffer.append("adding to decomposable but no pairs set: " + alpha + ", since subtuple = " + subtuple + "\n");
                    decomposable_but_no_pairs.add(alpha);
                    continue;
                } else {
                    // System.out.println("adding to indecomposable set: " + alpha + ", since subtuple = " + subtuple);
                    // if (print_outputs) pw.println("adding to indecomposable set: " + alpha);
                    if (print_outputs) no_pair_print_buffer.append("adding to indecomposable set: " + alpha + "\n");
                    indecomposable.add(alpha);
                    continue;
                }
            }
        }
    }

    public static void populate_indecomposable(Set<Tuple> V_set, Set<Tuple> indecomposable, int m) {
        for (Tuple tuple : V_set) {
            boolean has_subset = is_indecomposable_recursively(indecomposable, m, tuple, new ArrayList<Integer>(), 0, 0, 1);
            if (!has_subset) {
                indecomposable.add(tuple);
            }
        }
    }

    private static boolean is_indecomposable_recursively(Set<Tuple> indecomposable, int m, Tuple tuple, List<Integer> this_combination, int sum, int begin, int depth) {
        // only return true if subset found, else return false
        if (depth >= tuple.size()) return false;

        int size = tuple.size();
        for (int i = begin; i < size; ++i) {
            this_combination.add(tuple.get(i));
            sum += tuple.get(i);

            // System.out.println(this_combination.toString() + "   sum: " + sum); //DEBUG
            if (size % 2 == 0 && sum % m == 0) return true; // check if sum of tuple up to this element divides m

            // if not, check if any subsets that includes this subset is valid:
            if (is_indecomposable_recursively(indecomposable, m, tuple, this_combination, sum, i+1, depth+1)) return true;
            
            // none of subsets that includes this subset is valid, remove some elements and try other ones
            this_combination.remove(tuple.get(i));
            sum -= tuple.get(i);
        }
        return false;
    }

    public static void terminate_if_longer_than_n_seconds(int n) throws ProjectException {
        if (startTimeInNano == -1) {
            throw new ProjectException("Error: StartTimeInNano was never set.");
        }
        long elapsedInNano = System.nanoTime() - startTimeInNano;
        long elapsedInSeconds = elapsedInNano / 1000000000L;
        if (elapsedInSeconds > n) {
            skipThisMAndD = true;
            if (terminateIfTimeLimit) throw new ProjectException("Time limit exceeded " + n + " seconds.");
        }
    }

    public static String get_formatted_elapsed_time(long startTime, long endTime) {
        long elapsedTime = endTime - startTime; // in nano seconds (10^-9)
        
        // derive from nanoseconds elapsed from the start of the calculation operations of the program 
        // long tempSec  = elapsedTime / (1000*1000*1000);
        long allNanoSec  = elapsedTime;
        long allMicroSec =  elapsedTime / 1000;
        long allMiliSec  =  elapsedTime / (1000*1000);
        long allSec      = (elapsedTime / (1000*1000)) / 1000;
        long allMin      = (elapsedTime / (1000*1000)) / (1000*60);
        long allHour     = (elapsedTime / (1000*1000)) / (1000*60*60);
        long allDay      = (elapsedTime / (1000*1000)) / (1000*60*60*24);
        
        long nanoSec     =   allNanoSec % 1000; // in  nano seconds (10^-9)
        long microSec    =  allMicroSec % 1000; // in micro seconds (10^-6)
        long miliSec     =   allMiliSec % 1000; // in  mili seconds (10^-3)
        long sec         =       allSec % 60;
        long min         =       allMin % 60;
        long hour        =      allHour % 24;
        return String.format(
            "%d day%s, %d hour%s, %d minute%s, %d second%s, %d milisecond%s, %d microsecond%s, %d nanosecond%s", 
            allDay, plural(allDay), hour, plural(hour), min, plural(min), sec, plural(sec), 
            miliSec, plural(miliSec), microSec, plural(microSec), nanoSec, plural(nanoSec)
        );
    }

    public static void print_to_standard_output() {
        
    }

    public static String redString(Object obj) {
        String str = "";
        if (obj instanceof String) str = obj.toString();
        if (obj instanceof Integer) str = String.valueOf(obj);
        return "\u001b[31m" + str + "\u001b[0m";
    }
    
    public static String redString(String str, int num) {
        return "\u001b[31m" + str + num + "\u001b[0m";
    }

    public static String toStringSorted(Set<Tuple> set) {
        return toString(new TreeSet<Tuple>(set), ", ");
    }

    public static String toStringSorted(Set<Tuple> set, String delimiter) {
        return toString(new TreeSet<Tuple>(set), delimiter);
    }

    public static String toString(Set<Tuple> set) {
            return toString(set, ", ");
    }

    public static String toString(Set<Tuple> set, String delimiter) {
        StringBuilder sb = new StringBuilder("{");
        Iterator<Tuple> iter = set.iterator();
        if (iter.hasNext()) {
            sb.append(delimiter).append(iter.next().toString()); // element first
        }
        while (iter.hasNext()) {
            sb.append(delimiter).append(iter.next().toString()); // delimiter if theres another element
        }
        sb.append("\n}");
        return sb.toString();
    }

    
    public static String toString(int[] arr) throws ProjectException {
        return toString(arr, arr.length);
    }

    /**
     * 
     * @param arr
     * @param cut_off exclusive
     * @return
     * @throws ProjectException
     */
    public static String toString(int[] arr, int cut_off) throws ProjectException {
        if (cut_off < 0 || cut_off > arr.length) {
            throw new ProjectException("cut off = " + cut_off + " is invalid");
        }

        StringBuilder sb = new StringBuilder("[");
        for (int i = 0; i < cut_off-1; ++i) {
            sb.append(arr[i]).append(", ");
        }
        return sb.append(arr[cut_off-1]).append("]").toString();
    }

    public static String find_num_of_ascending_nonrepeating_tuples_in_U_set(Set<Integer> Z_mod_m_Z, int d) {
        BigInteger result = nCr(BigInteger.valueOf(Z_mod_m_Z.size()-1), BigInteger.valueOf(2*d));
        String str = result.toString();
        return str;
    }

    public static int sumOf(List<Integer> list) {
        int sum = 0;
        for (int i = 0; i < list.size(); ++i) {
            sum += list.get(i);
        }
        return sum;
    }

    public static int sumOf(int[] arr) {
        int sum = 0;
        for (int i = 0; i < arr.length; i++) {
            sum += arr[i];
        }
        return sum;
    }

    public static String plural(long num) {
        return num == 1 ? "" : "s";
    }

    public static String plural(int num) {
        return num == 1 ? "" : "s";
    }

    static boolean isPrime(int n) {
        if (n <= 1) return false;

        if (n == 2 || n == 3) return true;

        if (n % 2 == 0 || n % 3 == 0) return false;
        
        for (int i = 5; i <= Math.sqrt(n); i = i + 6) {
            if (n % i == 0 || n % (i + 2) == 0) {
                return false;
            }
        }

        return true;
    }

    /** Return the gcd of a and b using the euclidean algorithm
     * 
     * @param a - an integer
     * @param b - an integer
     * @return the greatest common divisor of a and b
     */
    public static int gcd(int a, int b) {
        if (a == 0) return b;
        return gcd(b % a, a);
    }

    public static BigInteger factorial(BigInteger n) {
        if (n.compareTo(BigInteger.ONE) < 1) return BigInteger.ONE;
        return n.multiply(factorial(n.subtract(BigInteger.ONE)));
    }

    public static BigInteger nCr(BigInteger n, BigInteger r) {
        BigInteger numer = factorial(n);
        BigInteger denom = (factorial(r).multiply(factorial(n.subtract(r))));
        return numer.divide(denom);
    }
}
