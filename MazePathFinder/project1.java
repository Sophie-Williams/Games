import java.util.regex.Matcher;
import java.util.regex.Pattern;
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.sql.Timestamp;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashMap;
import java.util.HashSet;
import java.util.Iterator;
import java.util.LinkedList;
import java.util.Scanner;

public class project1 {
	private String input;
	private final char sourceChar = 'S';
	private final char destineChar = 'D';
	private final char wallChar = '#';
	private final char pathChar = '.';
	private final char markChar = '*';
	private char[] allowedCharArr = {sourceChar,destineChar,wallChar,pathChar,'\n'};
	private Node sourceNode = new Node();
	private Node destineNode = new Node();
	private boolean pathFoundFlag = false;
	private ArrayList<String> rows = new ArrayList<String>();
	private LinkedList<Node> bsfQueue = new LinkedList<Node>();
//	private HashSet<Node> visitedNodeSet = new HashSet<Node>();
	private HashMap<Character,HashSet<Node>> teleporterMap = new HashMap<Character,HashSet<Node>>(); 
	public project1(String input) {
		this.input = input;
		this.rows = new ArrayList<String>(Arrays.asList(input.split("\n")));
	}
	public project1() {
		
	}
	public static String printTimeStamp() {
		 return (new Timestamp((new java.util.Date()).getTime())).toString();
	}
	public void printQueue(LinkedList<Node> bsfQueue) {
		System.out.println("Queue:: "+bsfQueue.size());
		/*System.out.println("------------Queue");
		for(Node node:bsfQueue) {
			System.out.println(node.toString()+"\n");
		}
		System.out.println("q----------------------");*/
	}	
	public void markVisited(Node node) {
		StringBuilder temp = new StringBuilder(rows.get(node.row));
		temp.setCharAt(node.col, markChar);
		rows.set(node.row, temp.toString());
	}
	public void addNode(Node parentNode, Node currentNode) {
//		if(!visitedNodeSet.contains(currentNode)) 
		{
//			visitedNodeSet.add(currentNode);
			markVisited(currentNode);
			bsfQueue.add(currentNode);
			currentNode.setParentNode(parentNode);
		}
		parentNode.getNodeLst().add(currentNode);
		if(currentNode.getData() == destineChar) {
			destineNode = currentNode;
			pathFoundFlag = true;
		}
//		printVisitedNodes();
	}
	public Node getTeleportedNode(HashSet<Node> set, Node node) {
		Iterator<Node> it = set.iterator();
		Node finalNode = null;
		while(it.hasNext() ) {
			Node temp = it.next();
			if(temp.getRow() == node.getRow() && temp.getCol() == node.getCol()) {
				continue;
			} else {
				finalNode = temp;
			}
		}
		return finalNode;
	}
	public void addNodeSpl(Node parentNode, Node currentNode) { // Have to improve
		String pattern ="\\d";
		boolean flag = false; // Normal or portal Scnerio
		{
			markVisited(currentNode);
			String temp = ""+currentNode.getData();
			if(temp.matches(pattern)) { // If true then it is a Teleporter
				HashSet<Node> set = teleporterMap.get(currentNode.getData());
				Node teleported = getTeleportedNode(set,currentNode);
				Node tempNode = currentNode; // Portal Entry
				tempNode.setParentNode(parentNode);
				tempNode.setPortal(true);
				teleported.setParentNode(currentNode); //Portal Exit
				currentNode = teleported;
				flag = true;
			}
			bsfQueue.add(currentNode);
			if(!flag) {
				currentNode.setParentNode(parentNode);
			}
		}
		parentNode.getNodeLst().add(currentNode);
		if(currentNode.getData() == destineChar) {
			destineNode = currentNode;
			pathFoundFlag = true;
		}
	}
	public void addAdjacentNodes(Node node) {
		int row = node.getRow();
		int col = node.getCol();
		{
			if(row != 0 ) {
				char data = rows.get(row-1).charAt(col);
				if(data!=wallChar && data!=markChar) {
					Node top = new Node(row-1,col,data);
					addNode(node, top);
					if(pathFoundFlag) {
						return;
					}
				}
			}
			if (col != rows.get(row).length()-1) {
				char data = rows.get(row).charAt(col+1);
				if(data!=wallChar  && data!=markChar) {
					Node right = new Node(row,col+1,data);
					addNode(node, right);
					if(pathFoundFlag) {
						return;
					}
				}
			}
			if(row != rows.size() -1 ) {
				char data = rows.get(row+1).charAt(col);
				if(data!=wallChar  && data!=markChar) {
					Node bottom = new Node(row+1, col, data);
					addNode(node, bottom);
					if(pathFoundFlag) {
						return;
					}
				}
			}
			if(col != 0) {
				char data = rows.get(row).charAt(col-1);
				if(data!=wallChar  && data!=markChar) {
					Node left = new Node(row, col-1, data);
					addNode(node, left);
					if(pathFoundFlag) {
						return;
					}
				}
			}
		}
	}
	public void addAdjacentNodesSpl(Node node) {
		int row = node.getRow();
		int col = node.getCol();
		{
			if(row != 0 ) {
				char data = rows.get(row-1).charAt(col);
				if(data!=wallChar && data!=markChar) {
					Node top = new Node(row-1,col,data);
					addNodeSpl(node, top);
					if(pathFoundFlag) {
						return;
					}
				}
			}
			if (col != rows.get(row).length()-1) {
				char data = rows.get(row).charAt(col+1);
				if(data!=wallChar && data!=markChar) {
					Node right = new Node(row,col+1,data);
					addNodeSpl(node, right);
					if(pathFoundFlag) {
						return;
					}
				}
			}
			if(row != rows.size() -1 ) {
				char data = rows.get(row+1).charAt(col);
				if(data!=wallChar && data!=markChar) {
					Node bottom = new Node(row+1, col, data);
					addNodeSpl(node, bottom);
					if(pathFoundFlag) {
						return;
					}
				}
			}
			if(col != 0) {
				char data = rows.get(row).charAt(col-1);
				if(data!=wallChar && data!=markChar) {
					Node left = new Node(row, col-1, data);
					addNodeSpl(node, left);
					if(pathFoundFlag) {
						return;
					}
				}
			}
		}		
	}
	public boolean validateTree() {
		for(int i=0;i<rows.size();i++) {
			String rowStr = rows.get(i);
			int sourceIdx = rowStr.indexOf(sourceChar);
			int destineIdx = rowStr.indexOf(destineChar);
			if(sourceIdx > -1)  {
				sourceNode.setCol(sourceIdx);
				sourceNode.setRow(i);
				sourceNode.setData(sourceChar);
			}
			if(destineIdx > -1) {
				destineNode.setCol(destineIdx);
				destineNode.setRow(i);
				destineNode.setData(destineChar);
			}
		}
		bsfQueue.add(sourceNode);
		markVisited(sourceNode);
		while (!bsfQueue.isEmpty()) {
			if(pathFoundFlag){
				break;
			}
			addAdjacentNodes(bsfQueue.pollFirst());
		}
		return pathFoundFlag;
	}
	public boolean validateTreeSpl() {
		String digitRegex = "\\d";
		Pattern pattern = Pattern.compile(digitRegex);
		for(int i=0;i<rows.size();i++) {
			String rowStr = rows.get(i);
			int sourceIdx = rowStr.indexOf(sourceChar);
			int destineIdx = rowStr.indexOf(destineChar);
			if(sourceIdx > -1)  {
				sourceNode.setCol(sourceIdx);
				sourceNode.setRow(i);
				sourceNode.setData(sourceChar);
			}
			if(destineIdx > -1) {
				destineNode.setCol(destineIdx);
				destineNode.setRow(i);
				destineNode.setData(destineChar);
			}
			Matcher matcher = pattern.matcher(rowStr);
			while(matcher.find()){
				char data = matcher.group(0).charAt(0);
				Node node = new Node(i, matcher.start(),data );
				if(!teleporterMap.containsKey(data)) {
					HashSet<Node> set = new HashSet<Node>();
					set.add(node);
					teleporterMap.put(data, set);
				} else {
					HashSet<Node> set = teleporterMap.get(data);
					set.add(node);
				}
			}
		}
		bsfQueue.add(sourceNode);
		markVisited(sourceNode);
		while (!bsfQueue.isEmpty()) {
			if(pathFoundFlag){
				break;
			}
			addAdjacentNodesSpl(bsfQueue.pollFirst());
		}
		return pathFoundFlag;
	}
	public boolean assertInput() {
		boolean flag = false;
			ArrayList<Character> uniqueLst = new ArrayList<Character>();
			HashSet<Character> allowedCharSet = new HashSet<Character>();
			HashSet<Character> inputCharSet = new HashSet<Character>();
			int wordSize=rows.get(0).length();
			int newLineCount = 0;
			boolean wordSizeFlag = true;
			for(char c: allowedCharArr) {
				allowedCharSet.add(c);
			}
			for(char c: input.toCharArray()) {
				if(c == sourceChar || c == destineChar) {
					uniqueLst.add(c);
				}
				if(c == '\n') {
					newLineCount++;
				}
				inputCharSet.add(c);
			}
			inputCharSet.removeAll(allowedCharSet);
			for (int i=0;i<rows.size();i++) {
				if(rows.get(i).length() != wordSize) {
					wordSizeFlag = false;
					break;
				}
			}
			/*System.out.println(uniqueLst.size());
			System.out.println(inputCharSet);
			Iterator<Character> it = inputCharSet.iterator();
			System.out.println("Char:: ");
			while (it.hasNext())
				System.out.println(it.next());
			System.out.println(wordSizeFlag);
			System.out.println(newLineCount-1);
			System.out.println(rows.size());*/
			if(uniqueLst.size() == 2 && inputCharSet.size() == 0 && wordSizeFlag && newLineCount-1==rows.size()) 
			{
				flag = true;
			}
		return flag;
	}
	public char calculatePath(Node node,Node parentNode) {
		char direction = 0;
		int row = node.getRow() - parentNode.getRow();
		int col = node.getCol() - parentNode.getCol();
		if(row == 1) {
			direction = 'D';
		} else if (row == -1){
			direction = 'U';
		}
		if(col == -1) {
			direction = 'L';
		} else if(col == 1) {
			direction = 'R';
		}				
		return direction;
	}
	public String getMazePath() {
		StringBuffer path = new StringBuffer();
		Node node = destineNode;
		while(node.getData() != sourceChar) {
			Node parentNode = node.getParentNode();
			if(!parentNode.isPortal()){
				path.append(calculatePath(node,parentNode));
			}
			node = parentNode;
		}
		path.reverse();
		return path.toString();		
	}
	public static void main(String[] args) {
		project1 project = new project1();
		try {
			int choice = Integer.parseInt(args[0]);
			char[] inputChar = new char[25010001];
			BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
			br.read(inputChar);
			String[] input  = String.valueOf(inputChar).split("\n");
			StringBuilder sb = new StringBuilder();
			for(int i=0;i<input.length;i++) {
				String row = input[i];
				if(!row.trim().isEmpty()) {
					project.rows.add(row.trim());
				}
				if(i!=input.length && row.indexOf(' ') > -1) {
					sb.append(row+"\n");
				} else {
					sb.append(row.trim()+"\n");
				}
			}
			project.input = sb.toString();
			
//			System.out.println(project.input);
//			System.out.println(input.length);
			switch(choice) {
				case 1:
					if(project.assertInput()) {
						System.out.println("YES");
					} else {
						System.out.println("NO");
					}
					break;
				case 2:
					if(project.validateTree()) {
						System.out.println("YES");
					} else {
						System.out.println("NO");
					}
					break;
				case 3:
					if(project.validateTree()) {
						System.out.println(project.getMazePath());
					} else {
						System.out.println("NO");
					}
					break;	
					case 4:
					if(project.validateTreeSpl()){
						System.out.println(project.getMazePath());
					} else {
						System.out.println("NO");
					}
					break;
				default:
					System.out.println("NO");
			}
		} catch(Exception e) {
			System.out.println("NO");
		}
//		System.out.println("END:: "+printTimeStamp());
	}
	class Node{
		public Node() {
		}
		public Node(int row, int col,char data) {
			this.row = row;
			this.col = col;
			this.data = data;
		}
		public Node(int row, int col,char data,boolean isPortal) {
			this.row = row;
			this.col = col;
			this.data = data;
			this.isPortal = isPortal;
		}
		private int row;
		private int col;
		private boolean isPortal=false;
		private char data;
		private ArrayList<Node> nodeLst = new ArrayList<Node>();
		private Node parentNode = null;
		public char getData() {
			return data;
		}
		public void setData(char data) {
			this.data = data;
		}
		public ArrayList<Node> getNodeLst() {
			return nodeLst;
		}
		public void setNodeLst(ArrayList<Node> nodeLst) {
			this.nodeLst = nodeLst;
		}
		public int getRow() {
			return row;
		}
		public void setRow(int row) {
			this.row = row;
		}
		public int getCol() {
			return col;
		}
		public void setCol(int col) {
			this.col = col;
		}
		public String toString() {
			return "("+this.row+","+this.col+") | Data: "+this.data;
		}
		public String nodeListToString() {
			StringBuffer nodeListStr = new StringBuffer();
			for(Node node:this.nodeLst) {
				nodeListStr.append(node.toString()+'\n');
			}
			return nodeListStr.toString();
			
		}
		@Override
		public int hashCode() {
			return this.col + this.row + this.data;
		}
		@Override
		public boolean equals(Object obj) {
			Node node = (Node)obj;
			if(this.row == node.row && this.col == node.col){
				return true;
			}
			return false;		 
		}
		public Node getParentNode() {
			return parentNode;
		}
		public void setParentNode(Node parentNode) {
			this.parentNode = parentNode;
		}
		public boolean isPortal() {
			return isPortal;
		}
		public void setPortal(boolean isPortal) {
			this.isPortal = isPortal;
		}
	}
}

