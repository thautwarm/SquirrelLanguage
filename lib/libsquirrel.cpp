
class printer{
public:
	std::string split;
	printer(std::string split){
		this->split=split;
	}
	template <typename T>
	void print(const T& t){
	std::cout << t <<split;
	}

	template <typename T, typename ... Args>
	void print(const T& t, Args ... args){
	print(t);
	print(args...);
}
};
