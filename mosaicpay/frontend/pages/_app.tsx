import { AppProps } from "next/app";
import Head from "next/head";

import "../src/app/globals.css";

const MyApp = ({ Component, pageProps }: AppProps) => {
	return (
		<>
			<Head>
				<title>MosaicPay</title>
			</Head>
			<Component {...pageProps} />
		</>
	);
};

export default MyApp;
