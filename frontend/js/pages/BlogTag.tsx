import React, { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import BlogList from "../components/BlogList";
import type { BlogPost } from "../api/types.gen";
import { BlogService } from "../api/services.gen";


const BlogTag = () => {
  const { tag } = useParams();
  const [posts, setPosts] = useState<BlogPost[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    setLoading(true);
    setError(null);

    BlogService.blogList({ tagsNome: tag })
      .then((data) => {
        setPosts(data.results);
      })
      .catch((error) => {
        console.error(error);
        setError("Erro ao buscar posts");
      })
      .finally(() => setLoading(false));
      }, [tag]);

  return (
    <>
      <h2 className="my-4 text-center">Artigos com a tag: #{tag}</h2>
      <BlogList posts={posts} loading={loading} error={error} />
    </>
  );
};

export default BlogTag;

