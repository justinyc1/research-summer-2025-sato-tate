package JC_code.javacode;

import java.util.List;
import java.util.ArrayList;

/** Tuple: A collection of elements that is: finite, ordered, immutable, fixed-length, allows repetition, and of type integer
 */
public class Tuple implements Comparable<Tuple> {
    private final int[] elements; // final: can't be change once assigned an to an array 
    public static Tuple EMPTY_TUPLE = new Tuple(0);

    private Tuple(int capacity) {
        elements = new int[capacity];
    }

    /** Create a Tuple from the contents of a List
     * 
     * @param list
     */
    public Tuple(List<Integer> list) {
        int capacity = list.size();
        elements = new int[capacity];
        for (int i = 0; i < capacity; ++i) {
            elements[i] = list.get(i);
        }
    }

    /** Create a Tuple from the contents of an array
     * 
     * @param arr
     */
    public Tuple(int[] arr) {
        int capacity = arr.length;
        elements = new int[capacity];
        for (int i = 0; i < capacity; ++i) {
            elements[i] = arr[i];
        }
    }

    /** Get the capacity/length of the tuple
     * 
     * @return the capacity/length of the tuple
     */
    public int size() {
        return elements.length;
    }

    /** Get an element by its index
     * 
     * @param index
     * @return
     */
    public int get(int index) {
        if (index < 0 || index >= elements.length) {
            throw new IndexOutOfBoundsException("Index out of bounds");
        }
        return elements[index];
    }

    /**
     * 
     * @return the sum of the elements
     */
    public int sum() {
        int sum = 0;
        for (int i = 0; i < elements.length; ++i) {
            sum += elements[i]; 
        }
        return sum;
    }

    /** Return a subtuple starting at index start (inclusive) until index end (exclusive)
     * 
     * @param start - inclusive
     * @param end - exclusive (one less than size)
     * @return
     */
    public Tuple getSubtuple(int start, int end) throws ProjectException {
        if (start >= end) throw new ProjectException("start = " + start + " and end = " + end + " index are invalid.");
        Tuple subtuple = new Tuple(end - start);
        for (int i = 0; i < subtuple.size(); ++i) {
            subtuple.elements[i] = this.elements[start+i];
        }
        return subtuple;
    }
    
    /** Return a subtuple starting at index start (inclusive) until the end of the tuple
     * 
     * @param start
     * @return
     * @throws ProjectException
     */
    public Tuple getSubtuple(int start) throws ProjectException {
        return getSubtuple(start, this.size());
    }

    public Tuple getNextAscendingTupleAfter(Tuple subtuple) throws ProjectException {
        int m = this.elements.length;
        int n = subtuple.elements.length;
        List<Integer> nextTuple = subtuple.toList();
        for (int i = n - 1; i >= 0; --i) { // each next tuple element from last to first
            if (nextTuple.get(i) >= this.get(m-(n-1-i)-1)) { // if ith last of next tuple is same or greater than ith of tuple
                continue;
            }
            int index = this.indexOf(subtuple.get(i)); // find index in tuple of value so get to the 'next' subtuple
            nextTuple.set(i, this.elements[index+1]);
            for (int j = i + 1; j < n; ++j) { // update subsequent elements to the lowest possible after the 'current' element
                nextTuple.set(j, this.elements[index+(j-(i+1))+2]);
            }
            return new Tuple(nextTuple);
        }
        return null;
    }

    /** Create a new Tuple of size = sum of input Tuples. Copy into the new Tuple in O(n) time
     * 
     * @param other
     * @return a new Tuple with the merged contents of the two input Tuples.
     */
    public Tuple merge(Tuple other) {
        Tuple result = new Tuple(this.elements.length + other.elements.length);
        int size = 0;
        for (int i = 0; i < this.elements.length; i++, size++) {
            result.elements[size] = this.elements[i];
        }
        for (int i = 0; i < other.elements.length; i++, size++) {
            result.elements[size] = other.elements[i];
        }
        return result;
    }

    /** Inverse a Tuple by m.
     *  
     *  A Tuple is considered inversed when each element is subtracted from m, and is listed in ascending order.
     * 
     *  i.e. m = 17, d = 4: (1, 2, 3, 5) -> (17-5, 17-3, 17-2, 17-1) = (12, 14, 15, 16)
     *  
     * @return a new Tuple that is inversed by m.
     */
    public Tuple inverse(int m) {
        int n = this.elements.length;
        Tuple result = new Tuple(n);
        for (int i = 0; i < n; i++) { // for each element in 'this'
            result.elements[n-1-i] = m - this.elements[i]; // 
        }
        return result;
    }

    /**Uses indexOf(), which implements binary search, to check if key exist in Tuple. (Tuple MUST be sorted in non-descending order)
     * 
     * @param key value to check if it exist in tuple
     * @return true if key is in the tuple, false otherwise
     */
    public boolean contains(int key) {
        int index = this.indexOf(key);
        return index == -1 ? false : true; 
    }

    /**Uses binary search to find the index of key in O(log n) time. (Tuple MUST be sorted in non-descending order)
     * 
     * @param key value to find the index of
     * @return index of key, or -1 if key is not in the tuple
     */
    public int indexOf(int key) {
        int low = 0;
        int high = this.elements.length - 1;
        while (low <= high) {
            int mid = low + (high - low)/2;
            if (this.elements[mid] == key) {//arr[1] == 1
                return mid;
            } else if (this.elements[mid] > key) {
                high = mid - 1;
            } else {
                low = mid + 1;
            }
        }
        return -1;
    }

    /** Print the tuple surrounded by parentheses
     * 
     */
    @Override
    public String toString() {
        return toString(", ");
    }

    public String toString(String delimiter) {
        int lastElementIndex = elements.length-1;
        StringBuilder sb = new StringBuilder("(");
        for (int i = 0; i < lastElementIndex; ++i) {
            sb.append(elements[i]).append(delimiter);
        }
        sb.append(elements[lastElementIndex]).append(")");
        return sb.toString();
    }


    /** Converts the tuple into a List
     * 
     * @return a List with the same content as the tuple
     */
    public List<Integer> toList() {
        List<Integer> newList = new ArrayList<>();
        for (int i = 0; i < elements.length; ++i) {
            newList.add(elements[i]);
        }
        return newList;
    }

    /** Compares a tuple to another object and returns true if both tuples are equal, equal as in for tuples a and b, a_i = b_i for all i
     * 
     */
    @Override
    public boolean equals(Object obj) {
        if (this == obj) return true; // they are the same object
        if (obj == null || getClass() != obj.getClass()) return false; // different class
        Tuple other = (Tuple) obj; // same class, cast obj and compare
        for (int i = 0; i < elements.length; ++i) {
            if (elements[i] != (other.elements[i])) {
                return false;
            }
        }
        return true;
    }

    @Override
    public int compareTo(Tuple other) { // other is a Tuple<E>
        if (Integer.compare(this.size(), ((Tuple)other).size()) != 0) { // if not same size, smaller come first
            return this.size() - ((Tuple)other).size();
        }
        for (int i = 0; i < Integer.min(this.size(), ((Tuple)other).size()); ++i) { // else compare every element
            if (Integer.compare(this.get(i), ((Tuple)other).get(i)) != 0) {
                return this.get(i) - ((Tuple)other).get(i);
            }
        }
        return 0;
    }
}