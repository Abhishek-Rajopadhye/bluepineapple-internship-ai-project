import PropTypes from "prop-types";
import ReactMarkdown from "react-markdown";
import remarkGemoji from "remark-gemoji";
import remarkMath from "remark-math";
import rehypeKatex from "rehype-katex";
import rehypeHighlight from "rehype-highlight";
import rehypeRaw from "rehype-raw";
import rehypeSlug from "rehype-slug";
import rehypeAutolinkHeadings from "rehype-autolink-headings";
import "katex/dist/katex.min.css";
import "highlight.js/styles/github.css";

const Message = ({ msg }) => {
    return (
        <div className={`flex ${msg.role === "user" ? "justify-end" : "justify-start"}`}>
            <span className={`px-4 py-2 rounded-lg text-sm border m-5 ${msg.role === "user" ? "bg-blue-500 border-blue-700 text-white mr-3" : "bg-gray-700 border-gray-500 text-white ml-3"}`}>
                <ReactMarkdown
                    remarkPlugins={[remarkGemoji, remarkMath]}
                    rehypePlugins={[rehypeKatex, rehypeHighlight, rehypeRaw, rehypeSlug, rehypeAutolinkHeadings]}
                >
                    {msg.text}
                </ReactMarkdown>
            </span>
        </div>
    );
};

Message.displayName = "Message";

Message.propTypes = {
    msg: PropTypes.shape({
        role: PropTypes.string.isRequired,
        text: PropTypes.string.isRequired,
    }).isRequired,
};

export { Message };
