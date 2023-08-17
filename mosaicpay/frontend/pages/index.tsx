import React from "react";
import { useRouter } from "next/router";

const HomePage = () => {
	const router = useRouter();

	React.useEffect(() => {
		router.push("/login");
	}, []);
};

export default HomePage;
