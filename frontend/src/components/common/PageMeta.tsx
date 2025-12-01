import { HelmetProvider, Helmet } from "react-helmet-async";

const APP_NAME = "Space Hub";

const PageMeta = ({
  title,
  description,
}: {
  title: string;
  description: string;
}) => (
  <Helmet>
    {/* Always show "Space Hub" in the browser tab */}
    <title>Space Hub</title>
    <meta name="description" content={description} />
  </Helmet>
);

export const AppWrapper = ({ children }: { children: React.ReactNode }) => (
  <HelmetProvider>{children}</HelmetProvider>
);

export default PageMeta;
