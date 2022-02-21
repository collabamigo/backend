import java.util.*;
import java.io.*;
public class AVL {
	public static class Tree{
		Tree left;
		Tree right;
		int data;
		int height;
		Tree(){
			this.left = null;
			this.right = null;
			this.height = 1;
		}
		
	}

	public static Tree head = null;

	static Tree insert_node(Tree root, int num){
		if(root == null){
			Tree new_node = new Tree();
			new_node.data = num;
			root = new_node;
			return root;
		}
		else if(root.data > num){
			root.left = insert_node(root.left, num);
		}
		else if(root.data < num)
			root.right = insert_node(root.right, num);
		else
			return root;

		root.height = 1 + (find_height(root.left) > find_height(root.right) ? find_height(root.left) : find_height(root.right));

		int balancing_factor = get_balancing_factor(root);

		if(balancing_factor > 1  && num < root.left.data){
			return rotate_right(root);
		}
		if(balancing_factor < -1 && num > root.right.data)
			return rotate_left(root);
		if(balancing_factor > 1 && num > root.left.data){
			root.left = rotate_left(root.left);
			return rotate_right(root);
		}
		if(balancing_factor < -1 && num < root.right.data){
			root.right = rotate_right(root.right);
			return rotate_left(root);
		}

		return root;

	}


	static Tree rotate_right(Tree root){
		Tree root_left = root.left;
		Tree below_left = root_left.right;
		root_left.right = root;
		root.left = below_left;
		root.height = (find_height(root.left) > find_height(root.right) ? find_height(root.left) : find_height(root.right)) + 1;
        root_left.height = (find_height(root_left.left) > find_height(root_left.right) ? find_height(root_left.left) : find_height(root_left.right)) + 1;

        return root_left;
	}

	static Tree rotate_left(Tree root){
		Tree below_right = root.right;
        Tree next_root = below_right.left;
 
        below_right.left = root;
        root.right = next_root;
 
        root.height = (find_height(root.left) > find_height(root.right) ? find_height(root.left) : find_height(root.right)) + 1;
        below_right.height = (find_height(below_right.left) > find_height(below_right.right) ? find_height(below_right.left) : find_height(below_right.right)) + 1;

        return below_right;
	}

	static int get_balancing_factor(Tree root){
		if(root == null)
			return 0;
		else
			return (find_height(root.left) - find_height(root.right));
	}

	static int find_height(Tree root){
		if (root == null)
			return 0;
		return root.height;

		}


	static Tree delete(Tree root, int num){
		if(root == null)
			return root;
		if(num < root.data){
			root.left = delete(root.left, num);
		}
		else if(num > root.data)
			root.right = delete(root.right, num);
		else{
			if(root.left == null && root.right == null)
				root = null;
			else if(root.left == null)
				root = root.right;
			else if(root.right == null)
				root = root.left;
			else{
			root.data = value_of_successor(root.right);
			root.right = delete(root.right, root.data);
		}
		}
		if(root == null)
			return root;
		int balancing_factor = get_balancing_factor(root);
        if (balancing_factor > 1 && get_balancing_factor(root.left) >= 0)
            return rotate_right(root);

        if (balancing_factor > 1 && get_balancing_factor(root.left) < 0)
        {
            root.left = rotate_left(root.left);
            return rotate_right(root);
        }
 
        if (balancing_factor < -1 && get_balancing_factor(root.right) <= 0)
            return rotate_left(root);
 
        if (balancing_factor < -1 && get_balancing_factor(root.right) > 0)
        {
            root.right = rotate_right(root.right);
            return rotate_left(root);
        }
 
        return root;
	}



	static int value_of_successor(Tree root){
		int min_value = root.data;
		while(root.left != null){
			min_value = root.left.data;
			root = root.left;
		}
		return min_value;
	}
/*
	static void preOrder(Tree node)
    {
        if (node != null)
        {
            System.out.print(node.data + " ");
            preOrder(node.left);
            preOrder(node.right);
        }
    }
    */

    static long find_min_node(Tree root){
    	if(root == null)
    		return -1;
    	long min = root.data;
    	long left_min = find_min_node(root.left);
    	long right_min = find_min_node(root.right);
    	if(left_min < min && left_min != -1)
    		min = left_min;
    	if(right_min < min && right_min != -1)
    		min = right_min;
    	return min;
    }

     static long find_max_node(Tree root){
    	if(root == null)
    		return -1;
    	long max = root.data;
    	long left_max = find_max_node(root.left);
    	long right_max = find_max_node(root.right);
    	if(left_max > max && left_max != -1)
    		max = left_max;
    	if(right_max > max && right_max != -1)
    		max = right_max;
    	return max;
    }


	public static void main(String[] args) throws Exception {
	Reader.init(System.in);
	int n = Reader.nextint();
	while(n-- > 0){
		String choice = Reader.next();
		if(choice.equals("INSERT")){
			int num = Reader.nextint();
			head = insert_node(head, num);
		}
		else if(choice.equals("DELETE")){
			int num = Reader.nextint();
			head = delete(head, num);
		}
		else if(choice.equals("MAX")){
			if(head == null)
				System.out.println("EMPTY");
			else
				System.out.println(find_max_node(head));
		}
		else{
			if(head == null)
				System.out.println("EMPTY");
			else
				System.out.println(find_min_node(head));
		}
		
	}
	}
}
class Reader {

    static BufferedReader reader;
    static StringTokenizer tokenizer;

    static void init(InputStream input) {
        reader = new BufferedReader(new InputStreamReader(input) );
        tokenizer = new StringTokenizer("");
    }

    static String next() throws IOException {
        while ( ! tokenizer.hasMoreTokens() ) {
            //TODO add check for eof if necessary
            tokenizer = new StringTokenizer(
                    reader.readLine() );
        }
        return tokenizer.nextToken();
    }

    static int nextint() throws IOException {
        return Integer.parseInt( next() );
    }

    static long nextlong() throws IOException {
        return Long.parseLong( next() );
    }

    static double nextdouble() throws IOException {
        return Double.parseDouble( next() );
    }

}